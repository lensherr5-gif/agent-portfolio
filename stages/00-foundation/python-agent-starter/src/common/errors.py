from __future__ import annotations


class AppError(Exception):
    """应用内统一错误基类，便于日志与监控聚合。"""

    def __init__(
        self,
        message: str,
        *,
        error_code: str,
        module: str,
        hint: str | None = None,
    ) -> None:
        super().__init__(message)
        # error_code/module/hint 会直接进入结构化日志字段。
        self.error_code = error_code
        self.module = module
        self.hint = hint


class ConfigError(AppError):
    """配置错误，例如缺少必要环境变量。"""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message,
            error_code="CFG_MISSING",
            module="config",
            hint=hint,
        )


class ParameterError(AppError):
    """参数错误，例如 run_id 格式非法。"""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message,
            error_code="ARG_INVALID",
            module="cli",
            hint=hint,
        )


class RuntimeAppError(AppError):
    """运行时错误占位类型，便于后续扩展。"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="RUNTIME_ERROR", module="runtime")
