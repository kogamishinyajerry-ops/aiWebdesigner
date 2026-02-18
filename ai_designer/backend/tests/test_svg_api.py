"""
Test SVG Generation Endpoints
"""

import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch


class TestSVGGeneration:
    """SVG generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_generate_svg_missing_description(self, client):
        """Test SVG generation without description"""
        response = await client.post(
            "/api/v1/svg/generate",
            json={}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_generate_svg_with_description(self, client):
        """Test SVG generation with description"""
        with patch('api.v1.endpoints.svg.svg_service') as mock_service:
            mock_result = {
                "svg_code": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><circle cx="256" cy="256" r="100"/></svg>',
                "width": 512,
                "height": 512,
                "style": "modern",
                "metadata": {"element_count": 1}
            }
            mock_service.text_to_svg = AsyncMock(return_value=mock_result)

            response = await client.post(
                "/api/v1/svg/generate",
                json={
                    "description": "A simple circle",
                    "style": "modern",
                    "width": 512,
                    "height": 512
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "svg_code" in data
            assert "<svg" in data["svg_code"]

    @pytest.mark.asyncio
    async def test_get_svg_styles(self, client):
        """Test getting SVG styles"""
        response = await client.get("/api/v1/svg/styles")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "styles" in data
        assert len(data["styles"]) > 0


class TestIconSetGeneration:
    """Icon set generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_generate_icon_set_missing_concept(self, client):
        """Test icon set generation without concept"""
        response = await client.post(
            "/api/v1/svg/icon-set"
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_generate_icon_set_with_concept(self, client):
        """Test icon set generation with concept"""
        with patch('api.v1.endpoints.svg.svg_service') as mock_service:
            mock_icons = [
                {
                    "name": "home",
                    "index": 1,
                    "svg_code": '<svg>...</svg>',
                    "width": 512,
                    "height": 512
                }
            ]
            mock_service.generate_icon_set = AsyncMock(return_value=mock_icons)

            response = await client.post(
                "/api/v1/svg/icon-set",
                params={
                    "concept": "navigation",
                    "count": 1,
                    "style": "outline"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "icons" in data
            assert len(data["icons"]) == 1
