from __future__ import annotations

import argparse
import re

from src.app.config import load_settings
from src.app.version import APP_VERSION
from src.common.errors import AppError, ParameterError
from src.common.logging_utils import generate_run_id, log_event

# 约束 run_id 可读且稳定，避免日志系统出现异常主键。
_RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,64}$")


def build_parser() -> argparse.ArgumentParser:
    """定义 CLI 参数：环境文件路径与运行 ID。"""
    parser = argparse.ArgumentParser(description="Minimal Python agent starter CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {APP_VERSION}")
    parser.add_argument("--env-file", default=".env", help="Path to .env file")
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id")
    return parser


def validate_run_id(run_id: str) -> None:
    """校验 run_id 格式，避免日志主键不可控。"""
    if not _RUN_ID_PATTERN.fullmatch(run_id):
        raise ParameterError("run_id must match [A-Za-z0-9_-]{3,64}")


def main(argv: list[str] | None = None) -> int:
    """CLI 入口：解析参数、加载配置、输出启动日志。"""
    args = build_parser().parse_args(argv)
    # 外部传入 run_id 便于排障复现；未传时自动生成。
    run_id = args.run_id or generate_run_id()

    try:
        if args.run_id:
            validate_run_id(args.run_id)
        settings = load_settings(args.env_file)
    except AppError as err:
        # 统一错误出口：保证失败也能结构化记录，便于检索告警。
        log_event(
            level="ERROR",
            message="app_failed",
            run_id=run_id,
            module=err.module,
            error_code=err.error_code,
            reason=str(err),
            hint=err.hint or "",
        )
        return 2

    log_event(
        level=settings.log_level,
        message="app_started",
        run_id=run_id,
        app_name=settings.app_name,
        app_env=settings.app_env,
    )
    return 0
