from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

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
    logger: Callable[[dict[str, object]], None] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> HttpResponse:
    """执行请求并在可重试错误场景下退避重试。"""
    policy = retry_policy or RetryPolicy()
    timeout_cfg = timeout_policy or TimeoutPolicy()

    attempt = 0
    while True:
        attempt += 1
        try:
            response = transport()
        except Exception as exc:  # noqa: BLE001 - 统一映射第三方异常
            mapped = map_external_error(exc)
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

        return response
