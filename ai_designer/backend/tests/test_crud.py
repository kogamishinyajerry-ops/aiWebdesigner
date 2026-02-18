"""
CRUD Operations Tests
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from crud.user import user_crud
from crud.project import project_crud
from crud.asset import asset_crud
from crud.generation import generation_crud
from models.user import User
from models.project import Project
from models.asset import Asset
from models.generation import Generation


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test creating a user"""
    user_data = {
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "name": "Test User"
    }

    user = await user_crud.create(db_session, user_data)

    assert user.email == user_data["email"]
    assert user.name == user_data["name"]
    assert user.id is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    """Test getting user by email"""
    # Create user first
    user_data = {
        "email": "find@example.com",
        "password_hash": "hashed_password",
        "name": "Find User"
    }
    await user_crud.create(db_session, user_data)

    # Find user
    user = await user_crud.get_by_email(db_session, "find@example.com")

    assert user is not None
    assert user.email == "find@example.com"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_project(db_session: AsyncSession):
    """Test creating a project"""
    # Create user first
    user_data = {
        "email": "project@example.com",
        "password_hash": "hashed_password",
        "name": "Project User"
    }
    user = await user_crud.create(db_session, user_data)

    # Create project
    project_data = {
        "user_id": user.id,
        "name": "Test Project",
        "description": "A test project",
        "type": "web",
        "status": "active"
    }

    project = await project_crud.create(db_session, project_data)

    assert project.name == project_data["name"]
    assert project.user_id == user.id


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_user_projects(db_session: AsyncSession):
    """Test getting user's projects"""
    # Create user
    user_data = {
        "email": "multi@example.com",
        "password_hash": "hashed_password",
        "name": "Multi Project User"
    }
    user = await user_crud.create(db_session, user_data)

    # Create multiple projects
    for i in range(3):
        project_data = {
            "user_id": user.id,
            "name": f"Project {i+1}",
            "description": f"Test project {i+1}",
            "type": "web",
            "status": "active"
        }
        await project_crud.create(db_session, project_data)

    # Get user's projects
    projects = await project_crud.get_by_user(db_session, user.id)

    assert len(projects) == 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_asset(db_session: AsyncSession):
    """Test creating an asset"""
    # Create user
    user_data = {
        "email": "asset@example.com",
        "password_hash": "hashed_password",
        "name": "Asset User"
    }
    user = await user_crud.create(db_session, user_data)

    # Create asset
    asset_data = {
        "user_id": user.id,
        "type": "image",
        "name": "Test Asset",
        "url": "https://example.com/image.png",
        "metadata": {"width": 1024, "height": 768}
    }

    asset = await asset_crud.create(db_session, asset_data)

    assert asset.name == asset_data["name"]
    assert asset.type == asset_data["type"]
    assert asset.url == asset_data["url"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_generation(db_session: AsyncSession):
    """Test creating a generation record"""
    # Create user
    user_data = {
        "email": "gen@example.com",
        "password_hash": "hashed_password",
        "name": "Generation User"
    }
    user = await user_crud.create(db_session, user_data)

    # Create project
    project_data = {
        "user_id": user.id,
        "name": "Test Project",
        "description": "Test",
        "type": "web",
        "status": "active"
    }
    project = await project_crud.create(db_session, project_data)

    # Create generation
    generation_data = {
        "user_id": user.id,
        "project_id": project.id,
        "type": "image",
        "prompt": "Test prompt",
        "status": "completed",
        "result_url": "https://example.com/result.png",
        "generation_time": 2.5
    }

    generation = await generation_crud.create(db_session, generation_data)

    assert generation.prompt == generation_data["prompt"]
    assert generation.status == generation_data["status"]
    assert generation.user_id == user.id


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_generation_status(db_session: AsyncSession):
    """Test updating generation status"""
    # Create user and generation
    user_data = {
        "email": "update@example.com",
        "password_hash": "hashed_password",
        "name": "Update User"
    }
    user = await user_crud.create(db_session, user_data)

    generation_data = {
        "user_id": user.id,
        "type": "image",
        "prompt": "Test prompt",
        "status": "processing"
    }
    generation = await generation_crud.create(db_session, generation_data)

    # Update status
    updated = await generation_crud.update_status(
        db_session,
        generation.id,
        "completed",
        result_url="https://example.com/result.png"
    )

    assert updated.status == "completed"
    assert updated.result_url == "https://example.com/result.png"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_soft_delete_asset(db_session: AsyncSession):
    """Test soft delete of asset"""
    # Create user and asset
    user_data = {
        "email": "delete@example.com",
        "password_hash": "hashed_password",
        "name": "Delete User"
    }
    user = await user_crud.create(db_session, user_data)

    asset_data = {
        "user_id": user.id,
        "type": "image",
        "name": "Test Asset",
        "url": "https://example.com/image.png"
    }
    asset = await asset_crud.create(db_session, asset_data)

    # Soft delete
    await asset_crud.delete(db_session, asset.id)

    # Check soft deleted
    deleted = await asset_crud.get(db_session, asset.id)
    assert deleted is None  # Soft deleted assets won't show in get()

    # But still exists in database
    result = await db_session.execute(
        select(Asset).where(Asset.id == asset.id)
    )
    db_asset = result.scalar_one()
    assert db_asset.deleted_at is not None
