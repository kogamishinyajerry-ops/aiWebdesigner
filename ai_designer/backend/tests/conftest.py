"""
Pytest Configuration
"""

import pytest
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from loguru import logger

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import settings
from core.database import Base, get_db
from main import app


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_designer_test"

# Test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

# Test session
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create test database session"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create test client with database override"""
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "Test123!@#",
        "name": "Test User"
    }


@pytest.fixture(scope="function")
async def test_project_data():
    """Test project data"""
    return {
        "name": "Test Project",
        "description": "A test project",
        "type": "web"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    logger.info("Configuring pytest tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers
    for item in items:
        if "async" in item.function.__name__:
            item.add_marker(pytest.mark.asyncio)
