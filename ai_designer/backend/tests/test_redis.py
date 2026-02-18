"""
Redis Cache Tests
"""

import pytest
import asyncio
from core.redis import cache


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_connect():
    """Test Redis connection"""
    await cache.connect()
    client = await cache.get_client()

    assert client is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_set_get():
    """Test Redis set and get"""
    await cache.set("test_key", "test_value", ttl=60)
    value = await cache.get("test_key")

    assert value == "test_value"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_json_set_get():
    """Test Redis JSON set and get"""
    data = {"key": "value", "number": 123}

    await cache.set("test_json", data, ttl=60)
    value = await cache.get("test_json")

    assert value == data


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_delete():
    """Test Redis delete"""
    await cache.set("delete_key", "value", ttl=60)
    await cache.delete("delete_key")

    value = await cache.get("delete_key")

    assert value is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_exists():
    """Test Redis exists"""
    await cache.set("exists_key", "value", ttl=60)

    exists = await cache.exists("exists_key")
    not_exists = await cache.exists("non_exists_key")

    assert exists is True
    assert not_exists is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_increment():
    """Test Redis increment"""
    await cache.increment("counter")
    await cache.increment("counter")
    await cache.increment("counter")

    value = await cache.get("counter")

    assert value == 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_redis_disconnect():
    """Test Redis disconnect"""
    await cache.disconnect()
    # Should not raise error
    await cache.disconnect()  # Multiple disconnects should be safe
