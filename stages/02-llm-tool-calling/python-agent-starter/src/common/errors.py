from __future__ import annotations


class AppError(Exception):
    """统一错误基类，携带可观测字段。"""

    def __init__(self, message: str, *, error_code: str, module: str, hint: str = "") -> None:
        super().__init__(message)
        self.error_code = error_code
        self.module = module
        self.hint = hint


class SchemaError(AppError):
    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message, error_code="SCHEMA_ERROR", module="schema", hint=hint)


class JsonGuardError(AppError):
    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message, error_code="JSON_PARSE_FAILED", module="json_guard", hint=hint)


class ToolPolicyError(AppError):
    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message, error_code="POLICY_BLOCKED", module="tool_policy", hint=hint)


class ToolExecutionError(AppError):
    def __init__(self, message: str, error_code: str = "TOOL_EXEC_ERROR", hint: str = "") -> None:
        super().__init__(message, error_code=error_code, module="tool_registry", hint=hint)


class ToolTimeoutError(ToolExecutionError):
    def __init__(self, message: str = "tool execution timeout") -> None:
        super().__init__(message, error_code="TOOL_TIMEOUT")


class LLMError(AppError):
    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message, error_code="LLM_ERROR", module="llm_client", hint=hint)
