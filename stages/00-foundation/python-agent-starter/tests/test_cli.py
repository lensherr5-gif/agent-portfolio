import json
from pathlib import Path

import pytest

from src.app.cli import build_parser, main, validate_run_id
from src.common.errors import ParameterError
from src.common.logging_utils import log_event


def test_parameter_missing_value() -> None:
    """缺少参数值时，argparse 应直接报错退出。"""
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--run-id"])


def test_invalid_run_id_parameter() -> None:
    """run_id 不合法时，应抛出统一参数错误。"""
    with pytest.raises(ParameterError):
        validate_run_id("invalid id!")


def test_log_event_has_required_fields(capsys: pytest.CaptureFixture[str]) -> None:
    """结构化日志必须包含核心字段，便于后续检索。"""
    log_event(level="INFO", message="test", run_id="abc123", module="unit")
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)

    assert payload["level"] == "INFO"
    assert payload["message"] == "test"
    assert payload["run_id"] == "abc123"
    assert payload["module"] == "unit"
    assert "ts" in payload


def test_help_output(capsys: pytest.CaptureFixture[str]) -> None:
    """--help 走标准退出码 0，并输出 usage。"""
    parser = build_parser()
    with pytest.raises(SystemExit) as err:
        parser.parse_args(["--help"])
    assert err.value.code == 0
    assert "usage:" in capsys.readouterr().out


def test_version_output(capsys: pytest.CaptureFixture[str]) -> None:
    """--version 输出版本号。"""
    parser = build_parser()
    with pytest.raises(SystemExit) as err:
        parser.parse_args(["--version"])
    assert err.value.code == 0
    assert "0.1.0" in capsys.readouterr().out


def test_main_returns_error_when_env_missing(tmp_path: Path) -> None:
    """关键配置缺失时，main 返回非 0 状态码。"""
    missing_env = tmp_path / ".env"
    missing_env.write_text("APP_ENV=dev\n", encoding="utf-8")

    rc = main(["--env-file", str(missing_env), "--run-id", "abc123"])
    assert rc == 2


def test_main_error_log_contains_hint(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """失败日志中应包含错误码与修复提示。"""
    bad_env = tmp_path / ".env"
    bad_env.write_text("APP_NAME=test-app\nAPP_ENV=dev\nLOG_LEVEL=BAD\n", encoding="utf-8")

    rc = main(["--env-file", str(bad_env), "--run-id", "abc123"])
    assert rc == 2
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert payload["error_code"] == "CFG_MISSING"
    assert payload["hint"] != ""
