"""
Test Health Endpoint
"""

import pytest
from fastapi import status


class TestHealth:
    """Health endpoint tests"""

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = await client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "AI Designer API"
        assert data["status"] == "running"


class TestAPIHealth:
    """API health tests"""

    @pytest.mark.asyncio
    async def test_api_v1_health(self, client):
        """Test API v1 health check"""
        response = await client.get("/api/v1/health/status")
        assert response.status_code == status.HTTP_200_OK
