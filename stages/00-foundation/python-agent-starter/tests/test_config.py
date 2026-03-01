from pathlib import Path

import pytest

from src.app.config import load_settings
from src.common.errors import ConfigError


def test_load_settings_from_env_file(tmp_path: Path) -> None:
    """正常配置文件可被正确解析。"""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=test-app\nAPP_ENV=test\nLOG_LEVEL=DEBUG\n",
        encoding="utf-8",
    )

    settings = load_settings(str(env_file))

    assert settings.app_name == "test-app"
    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"


def test_missing_required_env_var_raises_config_error(tmp_path: Path) -> None:
    """缺少必填配置应抛出配置错误。"""
    env_file = tmp_path / ".env"
    env_file.write_text("APP_ENV=dev\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load_settings(str(env_file))


def test_invalid_log_level_raises_config_error(tmp_path: Path) -> None:
    """非法日志等级应被白名单校验拦截。"""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=test-app\nAPP_ENV=dev\nLOG_LEVEL=VERBOSE\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_settings(str(env_file))
