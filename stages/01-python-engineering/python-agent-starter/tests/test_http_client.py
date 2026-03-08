from __future__ import annotations

import asyncio
import os
import random
from collections.abc import Iterator

import pytest

from src.common.errors import HttpRequestError, RequestError
from src.common.http_client import (
    CircuitBreaker,
    HttpResponse,
    RetryPolicy,
    TimeoutPolicy,
    build_httpx_get_transport,
    map_external_error,
    request_many_with_semaphore,
    request_with_retry,
)


def _seq_transport(items: list[object]) -> Iterator[object]:
    for item in items:
        yield item


def test_request_success() -> None:
    seq = _seq_transport([HttpResponse(status_code=200, body="ok")])

    def transport() -> HttpResponse:
        item = next(seq)
        assert isinstance(item, HttpResponse)
        return item

    response = request_with_retry(transport, run_id="run-001")
    assert response.status_code == 200
    assert response.body == "ok"


def test_retry_on_timeout_then_success() -> None:
    logs: list[dict[str, object]] = []
    seq = _seq_transport([TimeoutError("timeout"), HttpResponse(status_code=200, body="ok")])

    def transport() -> HttpResponse:
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    response = request_with_retry(
        transport,
        run_id="run-002",
        retry_policy=RetryPolicy(max_retries=2),
        logger=logs.append,
        sleep_fn=lambda _: None,
    )
    assert response.status_code == 200
    assert logs[0]["run_id"] == "run-002"
    assert logs[0]["error_code"] == "TIMEOUT"


def test_retry_on_429_then_success() -> None:
    logs: list[dict[str, object]] = []
    seq = _seq_transport([HttpRequestError(429), HttpResponse(status_code=200, body="ok")])

    def transport() -> HttpResponse:
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    response = request_with_retry(
        transport,
        run_id="run-003",
        retry_policy=RetryPolicy(max_retries=2),
        logger=logs.append,
        sleep_fn=lambda _: None,
    )
    assert response.status_code == 200
    assert logs[0]["error_code"] == "HTTP_429"


def test_fail_when_retry_exhausted_on_timeout() -> None:
    seq = _seq_transport([TimeoutError("t1"), TimeoutError("t2"), TimeoutError("t3")])

    def transport() -> HttpResponse:
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    with pytest.raises(RequestError) as exc:
        request_with_retry(
            transport,
            run_id="run-004",
            retry_policy=RetryPolicy(max_retries=2),
            sleep_fn=lambda _: None,
        )
    assert exc.value.error_code == "TIMEOUT"


def test_non_retriable_http_500_fail_fast() -> None:
    attempts = {"count": 0}
    seq = _seq_transport([HttpRequestError(500), HttpResponse(status_code=200, body="ok")])

    def transport() -> HttpResponse:
        attempts["count"] += 1
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    with pytest.raises(RequestError) as exc:
        request_with_retry(
            transport,
            run_id="run-005",
            retry_policy=RetryPolicy(max_retries=5, retriable_status_codes={429}),
            sleep_fn=lambda _: None,
        )
    assert exc.value.error_code == "HTTP_500"
    assert attempts["count"] == 1


def test_custom_retry_policy_no_retry_on_timeout() -> None:
    attempts = {"count": 0}
    seq = _seq_transport(
        [TimeoutError("connect timeout"), HttpResponse(status_code=200, body="ok")]
    )

    def transport() -> HttpResponse:
        attempts["count"] += 1
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    with pytest.raises(RequestError) as exc:
        request_with_retry(
            transport,
            run_id="run-006",
            retry_policy=RetryPolicy(max_retries=2, retriable_error_codes={"HTTP_429"}),
            sleep_fn=lambda _: None,
        )
    assert exc.value.error_code == "CONNECT_TIMEOUT"
    assert attempts["count"] == 1


def test_map_external_error_connection_error() -> None:
    mapped = map_external_error(ConnectionError("connection reset"))
    assert isinstance(mapped, RequestError)
    assert mapped.error_code == "NETWORK_ERROR"


def test_timeout_policy_fields_in_log() -> None:
    logs: list[dict[str, object]] = []
    seq = _seq_transport([TimeoutError("read timeout"), HttpResponse(status_code=200, body="ok")])

    def transport() -> HttpResponse:
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    request_with_retry(
        transport,
        run_id="run-007",
        retry_policy=RetryPolicy(max_retries=1),
        timeout_policy=TimeoutPolicy(connect_timeout_seconds=0.2, read_timeout_seconds=0.8),
        logger=logs.append,
        sleep_fn=lambda _: None,
    )
    assert logs[0]["connect_timeout_seconds"] == 0.2
    assert logs[0]["read_timeout_seconds"] == 0.8


@pytest.mark.skipif(
    os.getenv("STAGE01_HTTP_SMOKE") != "1",
    reason="set STAGE01_HTTP_SMOKE=1 to run real network smoke test",
)
def test_real_http_transport_smoke() -> None:
    transport = build_httpx_get_transport(
        "https://httpbin.org/get",
        timeout_policy=TimeoutPolicy(connect_timeout_seconds=2.0, read_timeout_seconds=4.0),
    )
    response = request_with_retry(
        transport,
        run_id="run-008",
        retry_policy=RetryPolicy(max_retries=1),
        sleep_fn=lambda _: None,
    )
    assert response.status_code == 200
    assert '"url"' in response.body


def test_circuit_breaker_open_then_fail_fast() -> None:
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_seconds=60.0)

    def transport() -> HttpResponse:
        raise TimeoutError("connect timeout")

    with pytest.raises(RequestError) as first:
        request_with_retry(
            transport,
            run_id="run-009",
            retry_policy=RetryPolicy(max_retries=0),
            circuit_breaker=breaker,
            sleep_fn=lambda _: None,
        )
    assert first.value.error_code == "CONNECT_TIMEOUT"

    with pytest.raises(RequestError) as second:
        request_with_retry(
            transport,
            run_id="run-010",
            retry_policy=RetryPolicy(max_retries=0),
            circuit_breaker=breaker,
            sleep_fn=lambda _: None,
        )
    assert second.value.error_code == "CONNECT_TIMEOUT"
    assert breaker.state.value == "open"

    with pytest.raises(RequestError) as fast_fail:
        request_with_retry(
            transport,
            run_id="run-011",
            retry_policy=RetryPolicy(max_retries=0),
            circuit_breaker=breaker,
            sleep_fn=lambda _: None,
        )
    assert fast_fail.value.error_code == "CIRCUIT_OPEN"


def test_request_many_with_semaphore_limits_concurrency() -> None:
    current = {"v": 0}
    max_seen = {"v": 0}
    lock = asyncio.Lock()

    def make_transport():
        async def _transport() -> HttpResponse:
            async with lock:
                current["v"] += 1
                max_seen["v"] = max(max_seen["v"], current["v"])
            await asyncio.sleep(0.02)
            async with lock:
                current["v"] -= 1
            return HttpResponse(status_code=200, body="ok")

        return _transport

    transports = [make_transport() for _ in range(8)]
    responses = asyncio.run(
        request_many_with_semaphore(
            transports,
            run_id="run-012",
            max_concurrency=3,
        )
    )
    assert len(responses) == 8
    assert max_seen["v"] <= 3


def test_fault_injection_random_timeout_and_429_recovery() -> None:
    rng = random.Random(7)
    state = {"attempt": 0}

    def transport() -> HttpResponse:
        state["attempt"] += 1
        # 前几次在 timeout/429/200 中随机，之后保证成功，便于验证可恢复。
        if state["attempt"] <= 6:
            x = rng.random()
            if x < 0.35:
                raise TimeoutError("read timeout")
            if x < 0.7:
                raise HttpRequestError(429)
        return HttpResponse(status_code=200, body="ok")

    response = request_with_retry(
        transport,
        run_id="run-013",
        retry_policy=RetryPolicy(max_retries=10, base_backoff_seconds=0.0),
        sleep_fn=lambda _: None,
    )
    assert response.status_code == 200
