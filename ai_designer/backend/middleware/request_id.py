"""
Request ID Middleware
为每个请求分配唯一ID，便于追踪和调试
"""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """为每个请求添加唯一ID"""

    async def dispatch(self, request: Request, call_next):
        # 生成或获取请求ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # 将请求ID存储在请求状态中
        request.state.request_id = request_id
        
        # 添加请求ID到日志上下文
        with logger.contextualize(request_id=request_id):
            logger.debug(f"Request started: {request.method} {request.url.path}")
            
            # 处理请求
            response = await call_next(request)
            
            # 添加请求ID到响应头
            response.headers["X-Request-ID"] = request_id
            
            logger.debug(f"Request completed: {response.status_code}")
            
            return response
