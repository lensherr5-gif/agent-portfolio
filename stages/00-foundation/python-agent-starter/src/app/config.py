from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.common.errors import ConfigError

# 限定日志等级，避免拼写错误导致日志策略失效。
_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass
class Settings:
    """从本地 .env 风格文件加载的应用配置。"""

    app_name: str
    app_env: str
    log_level: str = "INFO"


def _parse_env_file(path: Path) -> dict[str, str]:
    """将 env 文件中的 KEY=VALUE 行解析为字典。"""
    env: dict[str, str] = {}
    if not path.exists():
        return env

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def _require(parsed: dict[str, str], key: str) -> str:
    """读取必填配置项，不存在时给出可执行修复提示。"""
    value = parsed.get(key, "").strip()
    if not value:
        raise ConfigError(
            f"missing required env key: {key}",
            hint=f"set {key} in .env or pass --env-file",
        )
    return value


def load_settings(env_file: str = ".env") -> Settings:
    """加载配置；关键字段缺失时抛出配置错误。"""
    parsed = _parse_env_file(Path(env_file))
    # 对日志级别做标准化（大写）与白名单校验。
    log_level = parsed.get("LOG_LEVEL", "INFO").upper()
    if log_level not in _VALID_LOG_LEVELS:
        raise ConfigError(
            f"invalid LOG_LEVEL: {log_level}",
            hint=f"valid values: {sorted(_VALID_LOG_LEVELS)}",
        )

    return Settings(
        app_name=_require(parsed, "APP_NAME"),
        app_env=_require(parsed, "APP_ENV"),
        log_level=log_level,
    )
