"""
Logging Middleware
记录所有HTTP请求和响应的详细信息
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """记录HTTP请求和响应"""

    def __init__(self, app, skip_paths: list = None):
        super().__init__(app)
        self.skip_paths = skip_paths or ["/health", "/api/docs", "/api/redoc", "/"]

    async def dispatch(self, request: Request, call_next):
        # 跳过健康检查等路径
        if request.url.path in self.skip_paths:
            return await call_next(request)

        # 记录请求开始
        start_time = time.time()
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - Started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client": request.client.host if request.client else "unknown",
            }
        )

        # 处理请求
        try:
            response = await call_next(request)
        except Exception as e:
            # 记录异常
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} - Error: {str(e)}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                }
            )
            raise

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录响应
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - Completed {response.status_code} - {process_time:.3f}s",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": process_time,
                "client": request.client.host if request.client else "unknown",
            }
        )

        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        return response
