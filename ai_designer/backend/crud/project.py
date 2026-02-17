"""
Project CRUD operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.project import Project
from crud.base import CRUDBase


class CRUDProject(CRUDBase[Project]):
    """Project CRUD operations"""

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Get projects by user"""
        result = await db.execute(
            select(Project)
            .where(Project.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Project.updated_at.desc())
        )
        return result.scalars().all()

    async def get_with_designs(
        self,
        db: AsyncSession,
        id: str
    ) -> Optional[Project]:
        """Get project with its designs"""
        from sqlalchemy.orm import selectinload
        result = await db.execute(
            select(Project)
            .options(selectinload(Project.designs))
            .where(Project.id == id)
        )
        return result.scalar_one_or_none()


project_crud = CRUDProject(Project)
