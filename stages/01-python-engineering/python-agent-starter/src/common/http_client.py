from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Awaitable, Callable

from src.common.errors import (
    ConnectTimeoutError,
    HttpRequestError,
    NetworkError,
    ReadTimeoutError,
    RequestError,
)


@dataclass
class HttpResponse:
    status_code: int
    body: str


@dataclass
class RetryPolicy:
    """可配置重试策略。"""

    max_retries: int = 2
    base_backoff_seconds: float = 0.05
    backoff_multiplier: float = 2.0
    retriable_error_codes: set[str] = field(
        default_factory=lambda: {
            "CONNECT_TIMEOUT",
            "READ_TIMEOUT",
            "TIMEOUT",
            "NETWORK_ERROR",
            "HTTP_429",
        }
    )
    retriable_status_codes: set[int] = field(default_factory=lambda: {429})


@dataclass
class TimeoutPolicy:
    """网络调用超时分层配置。"""

    connect_timeout_seconds: float = 1.0
    read_timeout_seconds: float = 3.0


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"


@dataclass
class CircuitBreaker:
    """简化熔断器：失败次数超过阈值后快速失败。"""

    failure_threshold: int = 3
    recovery_timeout_seconds: float = 10.0
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    opened_at: float | None = None

    def before_request(self, now_fn: Callable[[], float] = time.time) -> None:
        if self.state != CircuitState.OPEN:
            return
        assert self.opened_at is not None
        if now_fn() - self.opened_at >= self.recovery_timeout_seconds:
            # 超过恢复窗口后允许一次请求探测。
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.opened_at = None
            return
        raise RequestError("circuit breaker is open", error_code="CIRCUIT_OPEN")

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def record_failure(self, now_fn: Callable[[], float] = time.time) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = now_fn()


def _backoff_seconds(policy: RetryPolicy, attempt: int) -> float:
    return policy.base_backoff_seconds * (policy.backoff_multiplier ** (attempt - 1))


def map_external_error(exc: Exception) -> RequestError:
    """将第三方异常统一映射为内部错误码。"""
    if isinstance(exc, RequestError):
        return exc

    if isinstance(exc, TimeoutError):
        lowered = str(exc).lower()
        if "connect" in lowered:
            return ConnectTimeoutError(str(exc))
        if "read" in lowered:
            return ReadTimeoutError(str(exc))
        return RequestError(str(exc) or "timeout", error_code="TIMEOUT")

    if isinstance(exc, ConnectionError):
        return NetworkError(str(exc) or "connection failed")

    name_lower = exc.__class__.__name__.lower()
    if "connecttimeout" in name_lower:
        return ConnectTimeoutError(str(exc))
    if "readtimeout" in name_lower:
        return ReadTimeoutError(str(exc))
    if "timeout" in name_lower:
        return RequestError(str(exc) or "timeout", error_code="TIMEOUT")
    if "networkerror" in name_lower or "connecterror" in name_lower:
        return NetworkError(str(exc) or "connection failed")

    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int):
        return HttpRequestError(status_code, str(exc) or "third-party http error")

    return RequestError(str(exc) or "third-party request error", error_code="THIRD_PARTY_ERROR")


def request_with_retry(
    transport: Callable[[], HttpResponse],
    *,
    run_id: str,
    retry_policy: RetryPolicy | None = None,
    timeout_policy: TimeoutPolicy | None = None,
    circuit_breaker: CircuitBreaker | None = None,
    logger: Callable[[dict[str, object]], None] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> HttpResponse:
    """执行请求并在可重试错误场景下退避重试。"""
    policy = retry_policy or RetryPolicy()
    timeout_cfg = timeout_policy or TimeoutPolicy()

    attempt = 0
    while True:
        attempt += 1
        if circuit_breaker is not None:
            circuit_breaker.before_request()
        try:
            response = transport()
        except Exception as exc:  # noqa: BLE001 - 统一映射第三方异常
            mapped = map_external_error(exc)
            if circuit_breaker is not None:
                circuit_breaker.record_failure()
            if logger:
                logger(
                    {
                        "run_id": run_id,
                        "module": "http_client",
                        "error_code": mapped.error_code,
                        "attempt": attempt,
                        "message": str(mapped),
                        "connect_timeout_seconds": timeout_cfg.connect_timeout_seconds,
                        "read_timeout_seconds": timeout_cfg.read_timeout_seconds,
                    }
                )
            should_retry = mapped.error_code in policy.retriable_error_codes
            if not should_retry or attempt > policy.max_retries:
                raise mapped from exc
            sleep_fn(_backoff_seconds(policy, attempt))
            continue

        if response.status_code in policy.retriable_status_codes:
            if circuit_breaker is not None:
                circuit_breaker.record_failure()
            if logger:
                logger(
                    {
                        "run_id": run_id,
                        "module": "http_client",
                        "error_code": f"HTTP_{response.status_code}",
                        "attempt": attempt,
                        "message": f"response status {response.status_code}",
                        "connect_timeout_seconds": timeout_cfg.connect_timeout_seconds,
                        "read_timeout_seconds": timeout_cfg.read_timeout_seconds,
                    }
                )
            if attempt > policy.max_retries:
                raise RequestError(
                    f"{response.status_code} response exceeded retries",
                    error_code=f"HTTP_{response.status_code}",
                )
            sleep_fn(_backoff_seconds(policy, attempt))
            continue

        if circuit_breaker is not None:
            circuit_breaker.record_success()
        return response


def build_httpx_get_transport(
    url: str,
    *,
    timeout_policy: TimeoutPolicy | None = None,
    headers: dict[str, str] | None = None,
) -> Callable[[], HttpResponse]:
    """构建真实联网 GET transport（基于 httpx）。"""
    timeout_cfg = timeout_policy or TimeoutPolicy()

    def _transport() -> HttpResponse:
        import httpx

        timeout = httpx.Timeout(
            connect=timeout_cfg.connect_timeout_seconds,
            read=timeout_cfg.read_timeout_seconds,
            write=timeout_cfg.read_timeout_seconds,
            pool=timeout_cfg.connect_timeout_seconds,
        )
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
        return HttpResponse(status_code=response.status_code, body=response.text)

    return _transport


async def request_many_with_semaphore(
    transports: list[Callable[[], Awaitable[HttpResponse]]],
    *,
    run_id: str,
    max_concurrency: int = 3,
) -> list[HttpResponse]:
    """并发执行多个请求，通过 Semaphore 限制瞬时并发。"""
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _run_one(transport: Callable[[], Awaitable[HttpResponse]]) -> HttpResponse:
        async with semaphore:
            return await transport()

    return await asyncio.gather(*[_run_one(t) for t in transports])
