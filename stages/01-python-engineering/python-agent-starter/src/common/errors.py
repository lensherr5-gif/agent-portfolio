from __future__ import annotations


class AppError(Exception):
    """应用统一错误基类，包含可观测所需字段。"""

    def __init__(self, message: str, *, error_code: str, module: str) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.module = module


class ConfigError(AppError):
    """配置类错误。"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="CFG_ERROR", module="config")


class RequestError(AppError):
    """网络请求类错误。"""

    def __init__(self, message: str, *, error_code: str = "REQ_ERROR") -> None:
        super().__init__(message, error_code=error_code, module="http_client")


class BusinessError(AppError):
    """业务语义错误（非网络层）。"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="BUSINESS_ERROR", module="business")


class HttpRequestError(RequestError):
    """带状态码的 HTTP 请求错误。"""

    def __init__(self, status_code: int, message: str = "http request failed") -> None:
        self.status_code = status_code
        super().__init__(f"{message}: status={status_code}", error_code="HTTP_ERROR")
