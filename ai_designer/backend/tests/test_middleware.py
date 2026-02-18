"""
Middleware Tests
"""

import pytest
from httpx import AsyncClient
from middleware.error_handler import (
    ValidationError,
    NotFoundError,
    RateLimitError
)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_request_id_middleware(client: AsyncClient):
    """Test request ID middleware"""
    response = await client.get("/health")

    assert "x-request-id" in response.headers
    assert len(response.headers["x-request-id"]) == 36  # UUID length


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cors_middleware(client: AsyncClient):
    """Test CORS middleware"""
    response = await client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_rate_limit_middleware(client: AsyncClient):
    """Test rate limiting"""
    # Make multiple requests
    responses = []
    for _ in range(5):
        response = await client.get("/health")
        responses.append(response.status_code)

    # Should all succeed (assuming rate limit > 5)
    assert all(status == 200 for status in responses)


@pytest.mark.unit
def test_custom_errors():
    """Test custom error classes"""
    # ValidationError
    error = ValidationError("Validation failed", {"field": "required"})
    assert error.status_code == 422
    assert error.error_code == "VALIDATION_ERROR"

    # NotFoundError
    error = NotFoundError("Resource not found", "user")
    assert error.status_code == 404
    assert error.error_code == "NOT_FOUND"

    # RateLimitError
    error = RateLimitError("Too many requests", 60)
    assert error.status_code == 429
    assert error.error_code == "RATE_LIMIT_EXCEEDED"
