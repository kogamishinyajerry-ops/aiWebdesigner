"""
User CRUD operations
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from crud.base import CRUDBase


class CRUDUser(CRUDBase[User]):
    """User CRUD operations"""

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None
    ) -> User:
        """Create a new user"""
        db_obj = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser


user_crud = CRUDUser(User)
