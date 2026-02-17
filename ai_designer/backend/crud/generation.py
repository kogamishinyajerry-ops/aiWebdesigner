"""
Generation CRUD operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta

from models.generation import Generation, GenerationCache
from crud.base import CRUDBase


class CRUDGeneration(CRUDBase[Generation]):
    """Generation CRUD operations"""

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Generation]:
        """Get generations by user"""
        result = await db.execute(
            select(Generation)
            .where(Generation.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Generation.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_status(
        self,
        db: AsyncSession,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Generation]:
        """Get generations by status"""
        result = await db.execute(
            select(Generation)
            .where(Generation.status == status)
            .offset(skip)
            .limit(limit)
            .order_by(Generation.created_at.desc())
        )
        return result.scalars().all()

    async def create_pending(
        self,
        db: AsyncSession,
        user_id: str,
        type: str,
        model: str,
        prompt: str,
        parameters: dict
    ) -> Generation:
        """Create a pending generation"""
        db_obj = Generation(
            user_id=user_id,
            type=type,
            model=model,
            prompt=prompt,
            parameters=parameters,
            status="pending"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_status(
        self,
        db: AsyncSession,
        id: str,
        status: str,
        result_url: Optional[str] = None,
        result_content: Optional[str] = None,
        generation_time: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> Optional[Generation]:
        """Update generation status"""
        obj = await self.get(db, id)
        if obj:
            obj.status = status
            if result_url:
                obj.result_url = result_url
            if result_content:
                obj.result_content = result_content
            if generation_time:
                obj.generation_time = generation_time
            if error_message:
                obj.error_message = error_message
            await db.commit()
            await db.refresh(obj)
        return obj


class CRUDGenerationCache(CRUDBase[GenerationCache]):
    """Generation Cache CRUD operations"""

    async def get_by_key(
        self,
        db: AsyncSession,
        cache_key: str
    ) -> Optional[GenerationCache]:
        """Get cache by key"""
        # Check if cache is expired
        result = await db.execute(
            select(GenerationCache)
            .where(GenerationCache.cache_key == cache_key)
            .where(GenerationCache.expires_at > datetime.utcnow())
        )
        return result.scalar_one_or_none()

    async def create_cache(
        self,
        db: AsyncSession,
        cache_key: str,
        type: str,
        prompt_hash: str,
        parameters_hash: str,
        result_url: Optional[str] = None,
        result_content: Optional[str] = None,
        metadata: Optional[dict] = None,
        ttl: int = 3600
    ) -> GenerationCache:
        """Create a cache entry"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        db_obj = GenerationCache(
            cache_key=cache_key,
            type=type,
            prompt_hash=prompt_hash,
            parameters_hash=parameters_hash,
            result_url=result_url,
            result_content=result_content,
            metadata=metadata,
            expires_at=expires_at
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def increment_hit(self, db: AsyncSession, id: str) -> Optional[GenerationCache]:
        """Increment cache hit count"""
        obj = await self.get(db, id)
        if obj:
            obj.hit_count += 1
            await db.commit()
            await db.refresh(obj)
        return obj

    async def cleanup_expired(self, db: AsyncSession) -> int:
        """Delete expired cache entries"""
        from sqlalchemy import delete
        stmt = delete(GenerationCache).where(GenerationCache.expires_at < datetime.utcnow())
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount


generation_crud = CRUDGeneration(Generation)
generation_cache_crud = CRUDGenerationCache(GenerationCache)
