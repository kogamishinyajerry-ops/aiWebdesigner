"""
Rate Limit Middleware
基于Redis的API速率限制
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from loguru import logger
import time
from typing import Optional
from redis.asyncio import Redis
from core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """API速率限制中间件"""

    def __init__(self, app, redis_client: Optional[Redis] = None):
        super().__init__(app)
        self.redis = redis_client
        self.default_limit = settings.RATE_LIMIT_REQUESTS
        self.default_window = settings.RATE_LIMIT_WINDOW

    async def dispatch(self, request: Request, call_next):
        # 跳过健康检查
        if request.url.path in ["/health", "/api/docs", "/api/redoc", "/"]:
            return await call_next(request)

        # 获取客户端标识
        client_id = self._get_client_id(request)

        # 获取速率限制
        limit, window = self._get_rate_limit(request)

        # 检查速率限制
        if not await self._check_rate_limit(client_id, limit, window):
            logger.warning(
                f"Rate limit exceeded for {client_id} on {request.url.path}"
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "detail": f"Too many requests. Limit: {limit} requests per {window} seconds",
                    "retry_after": window,
                }
            )

        return await call_next(request)

    def _get_client_id(self, request: Request) -> str:
        """获取客户端标识"""
        # 优先使用X-Forwarded-For头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # 使用X-Real-IP头
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # 使用直接连接的IP
        if request.client:
            return request.client.host

        return "unknown"

    def _get_rate_limit(self, request: Request) -> tuple[int, int]:
        """获取速率限制配置"""
        # 根据端点类型设置不同的限制
        path = request.url.path

        # 图像生成端点 - 更严格的限制
        if "/generate/image" in path:
            return 10, 60  # 10次/分钟

        # SVG生成端点
        if "/generate/svg" in path:
            return 30, 60  # 30次/分钟

        # 代码生成端点
        if "/generate/code" in path:
            return 20, 60  # 20次/分钟

        # 默认限制
        return self.default_limit, self.default_window

    async def _check_rate_limit(
        self,
        client_id: str,
        limit: int,
        window: int
    ) -> bool:
        """检查是否超过速率限制"""
        if not self.redis:
            # 如果没有Redis，跳过速率限制
            return True

        key = f"rate_limit:{client_id}:{self._get_window_key(window)}"
        current_time = int(time.time())

        try:
            # 使用Redis Sorted Set实现滑动窗口
            # 移除窗口外的请求
            await self.redis.zremrangebyscore(key, 0, current_time - window)

            # 获取当前请求数
            current_count = await self.redis.zcard(key)

            # 检查是否超过限制
            if current_count >= limit:
                return False

            # 添加当前请求
            await self.redis.zadd(key, {str(current_time): current_time})

            # 设置过期时间
            await self.redis.expire(key, window)

            return True

        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Redis出错时，允许请求通过
            return True

    def _get_window_key(self, window: int) -> str:
        """获取时间窗口key"""
        return f"{int(time.time() // window)}"
