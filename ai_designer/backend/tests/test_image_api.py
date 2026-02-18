"""
Test Image Generation Endpoints
"""

import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch


class TestImageGeneration:
    """Image generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_get_available_styles(self, client):
        """Test getting available styles"""
        response = await client.get("/api/v1/image/styles")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "presets" in data
        assert len(data["presets"]) > 0
        # Check for known styles
        style_ids = [p["id"] for p in data["presets"]]
        assert "modern" in style_ids
        assert "minimal" in style_ids

    @pytest.mark.asyncio
    async def test_generate_image_missing_prompt(self, client):
        """Test image generation with missing prompt"""
        response = await client.post(
            "/api/v1/image/generate",
            json={}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_generate_image_with_prompt(self, client):
        """Test image generation with valid prompt"""
        # Mock the image service since we don't have GPU
        with patch('api.v1.endpoints.image.image_service') as mock_service:
            # Create mock response
            mock_result = {
                "image_data": b"fake_image_data",
                "width": 1280,
                "height": 720,
                "aesthetic_score": 0.85
            }
            mock_service.generate_hero_banner.return_value = mock_result

            response = await client.post(
                "/api/v1/image/generate",
                json={
                    "prompt": "A modern hero banner",
                    "style": "modern",
                    "size": "hero_medium"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "image_url" in data


class TestIconGeneration:
    """Icon generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_generate_icons_missing_concept(self, client):
        """Test icon generation without concept"""
        response = await client.post(
            "/api/v1/image/icons"
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_generate_icons_with_concept(self, client):
        """Test icon generation with concept"""
        with patch('api.v1.endpoints.image.image_service') as mock_service:
            # Create mock icons
            mock_icons = [
                {
                    "image_data": b"fake_icon_data",
                    "concept": "home",
                    "style": "outline",
                    "variant": 1,
                    "width": 512,
                    "height": 512
                }
            ]
            mock_service.generate_icon.return_value = mock_icons

            response = await client.post(
                "/api/v1/image/icons",
                params={
                    "concept": "navigation",
                    "style": "outline",
                    "count": 1
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "icons" in data
            assert len(data["icons"]) == 1


class TestBackgroundGeneration:
    """Background generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_generate_background(self, client):
        """Test background generation"""
        with patch('api.v1.endpoints.image.image_service') as mock_service:
            mock_result = {
                "image_data": b"fake_background_data",
                "style": "gradient",
                "width": 1280,
                "height": 720
            }
            mock_service.generate_background.return_value = mock_result

            response = await client.post(
                "/api/v1/image/background",
                params={
                    "style": "gradient",
                    "complexity": "medium"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "image_url" in data
