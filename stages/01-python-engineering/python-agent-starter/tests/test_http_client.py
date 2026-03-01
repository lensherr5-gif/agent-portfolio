from __future__ import annotations

from collections.abc import Iterator

import pytest

from src.common.errors import HttpRequestError, RequestError
from src.common.http_client import (
    HttpResponse,
    RetryPolicy,
    TimeoutPolicy,
    map_external_error,
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
    seq = _seq_transport([TimeoutError("connect timeout"), HttpResponse(status_code=200, body="ok")])

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
