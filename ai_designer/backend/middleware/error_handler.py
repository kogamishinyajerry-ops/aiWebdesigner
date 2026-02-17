"""
Error Handler Middleware
统一处理所有异常和错误响应
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError


class APIError(Exception):
    """自定义API错误基类"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Optional[str] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        super().__init__(message)


class ValidationError(APIError):
    """验证错误"""

    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class NotFoundError(APIError):
    """资源未找到"""

    def __init__(self, message: str = "Resource not found", detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND"
        )


class ConflictError(APIError):
    """资源冲突"""

    def __init__(self, message: str = "Resource conflict", detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT"
        )


class UnauthorizedError(APIError):
    """未授权"""

    def __init__(self, message: str = "Unauthorized", detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED"
        )


class RateLimitError(APIError):
    """速率限制"""

    def __init__(self, message: str = "Rate limit exceeded", detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED"
        )


def create_error_response(
    error: APIError,
    request_id: str = "unknown"
) -> JSONResponse:
    """创建标准错误响应"""

    content: Dict[str, Any] = {
        "error": error.message,
        "error_code": error.error_code,
        "request_id": request_id,
    }

    if error.detail:
        content["detail"] = error.detail

    return JSONResponse(
        status_code=error.status_code,
        content=content
    )


class ErrorHandlerMiddleware:
    """错误处理中间件"""

    def __init__(self, app):
        self.app = app
        self._register_exception_handlers()

    def _register_exception_handlers(self):
        """注册异常处理器"""

        # 自定义API错误
        @self.app.exception_handler(APIError)
        async def api_error_handler(request: Request, exc: APIError):
            request_id = getattr(request.state, "request_id", "unknown")
            logger.warning(
                f"[{request_id}] API Error: {exc.error_code} - {exc.message}"
            )
            return create_error_response(exc, request_id)

        # FastAPI验证错误
        @self.app.exception_handler(RequestValidationError)
        async def validation_error_handler(request: Request, exc: RequestValidationError):
            request_id = getattr(request.state, "request_id", "unknown")
            logger.warning(
                f"[{request_id}] Validation Error: {exc.errors()}"
            )
            
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": "Validation failed",
                    "error_code": "VALIDATION_ERROR",
                    "request_id": request_id,
                    "detail": exc.errors(),
                }
            )

        # 数据库错误
        @self.app.exception_handler(SQLAlchemyError)
        async def database_error_handler(request: Request, exc: SQLAlchemyError):
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(f"[{request_id}] Database Error: {str(exc)}")
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Database operation failed",
                    "error_code": "DATABASE_ERROR",
                    "request_id": request_id,
                }
            )

        # 未处理的异常
        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(
                f"[{request_id}] Unhandled Exception: {type(exc).__name__} - {str(exc)}",
                exc_info=True
            )
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "error_code": "INTERNAL_ERROR",
                    "request_id": request_id,
                }
            )
