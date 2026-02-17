"""
Asset CRUD operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from models.asset import Asset
from crud.base import CRUDBase


class CRUDAsset(CRUDBase[Asset]):
    """Asset CRUD operations"""

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Asset]:
        """Get assets by user"""
        result = await db.execute(
            select(Asset)
            .where(Asset.user_id == user_id)
            .where(Asset.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .order_by(Asset.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_type(
        self,
        db: AsyncSession,
        user_id: str,
        asset_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Asset]:
        """Get assets by type"""
        result = await db.execute(
            select(Asset)
            .where(
                and_(
                    Asset.user_id == user_id,
                    Asset.type == asset_type,
                    Asset.is_deleted == False
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Asset.created_at.desc())
        )
        return result.scalars().all()

    async def soft_delete(
        self,
        db: AsyncSession,
        id: str
    ) -> Optional[Asset]:
        """Soft delete an asset"""
        from datetime import datetime
        obj = await self.get(db, id)
        if obj:
            obj.is_deleted = True
            obj.deleted_at = datetime.utcnow()
            await db.commit()
            await db.refresh(obj)
        return obj


asset_crud = CRUDAsset(Asset)
