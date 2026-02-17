"""
Redis cache configuration and utilities
"""

from redis.asyncio import Redis, from_url
from typing import Optional, Any
import json
from loguru import logger
from core.config import settings


class RedisCache:
    """Redis缓存管理器"""

    def __init__(self):
        self._client: Optional[Redis] = None

    async def connect(self):
        """连接到Redis"""
        try:
            self._client = from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self._client.ping()
            logger.info("✅ Redis connected successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            self._client = None

    async def disconnect(self):
        """断开Redis连接"""
        if self._client:
            await self._client.close()
            logger.info("Redis disconnected")

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self._client:
            return None

        try:
            value = await self._client.get(key)
            if value is not None:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """设置缓存"""
        if not self._client:
            return False

        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            await self._client.set(key, value, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._client:
            return False

        try:
            await self._client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """检查key是否存在"""
        if not self._client:
            return False

        try:
            return await self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """递增计数器"""
        if not self._client:
            return None

        try:
            return await self._client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Redis increment error: {e}")
            return None

    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        if not self._client:
            return False

        try:
            return await self._client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis expire error: {e}")
            return False

    async def get_client(self) -> Optional[Redis]:
        """获取Redis客户端实例"""
        return self._client


# 全局Redis缓存实例
cache = RedisCache()


async def get_cache() -> RedisCache:
    """依赖注入: 获取缓存实例"""
    return cache
