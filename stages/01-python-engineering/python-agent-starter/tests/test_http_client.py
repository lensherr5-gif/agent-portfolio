from __future__ import annotations

from collections.abc import Iterator

import pytest

from src.common.errors import HttpRequestError, RequestError
from src.common.http_client import HttpResponse, request_with_retry


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
        max_retries=2,
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
        max_retries=2,
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
        request_with_retry(transport, run_id="run-004", max_retries=2, sleep_fn=lambda _: None)
    assert exc.value.error_code == "TIMEOUT"
