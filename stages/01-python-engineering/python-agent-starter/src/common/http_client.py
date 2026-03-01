from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from src.common.errors import RequestError


@dataclass
class HttpResponse:
    status_code: int
    body: str


def request_with_retry(
    transport: Callable[[], HttpResponse],
    *,
    run_id: str,
    max_retries: int = 2,
    base_backoff_seconds: float = 0.05,
    logger: Callable[[dict[str, object]], None] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> HttpResponse:
    """执行请求并在超时/429场景重试。"""
    attempt = 0
    while True:
        attempt += 1
        try:
            response = transport()
        except TimeoutError as exc:
            if logger:
                logger(
                    {
                        "run_id": run_id,
                        "module": "http_client",
                        "error_code": "TIMEOUT",
                        "attempt": attempt,
                        "message": str(exc),
                    }
                )
            if attempt > max_retries:
                raise RequestError("timeout exceeded retries", error_code="TIMEOUT") from exc
            sleep_fn(base_backoff_seconds * (2 ** (attempt - 1)))
            continue
        except RequestError as exc:
            # 仅对 429 做重试；其他错误直接抛出。
            if getattr(exc, "status_code", None) != 429:
                if logger:
                    logger(
                        {
                            "run_id": run_id,
                            "module": "http_client",
                            "error_code": exc.error_code,
                            "attempt": attempt,
                            "message": str(exc),
                        }
                    )
                raise

            if logger:
                logger(
                    {
                        "run_id": run_id,
                        "module": "http_client",
                        "error_code": "HTTP_429",
                        "attempt": attempt,
                        "message": str(exc),
                    }
                )
            if attempt > max_retries:
                raise RequestError("429 exceeded retries", error_code="HTTP_429") from exc
            sleep_fn(base_backoff_seconds * (2 ** (attempt - 1)))
            continue

        if response.status_code == 429:
            if logger:
                logger(
                    {
                        "run_id": run_id,
                        "module": "http_client",
                        "error_code": "HTTP_429",
                        "attempt": attempt,
                        "message": "response status 429",
                    }
                )
            if attempt > max_retries:
                raise RequestError("429 response exceeded retries", error_code="HTTP_429")
            sleep_fn(base_backoff_seconds * (2 ** (attempt - 1)))
            continue

        return response
