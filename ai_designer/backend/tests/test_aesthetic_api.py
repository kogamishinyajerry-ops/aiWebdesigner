"""
Test Aesthetic Engine Endpoints
"""

import pytest
from fastapi import status


class TestColorRecommendation:
    """Color recommendation endpoint tests"""

    @pytest.mark.asyncio
    async def test_recommend_colors(self, client):
        """Test color recommendation"""
        response = await client.post(
            "/api/v1/aesthetic/colors/recommend",
            json={
                "style": "modern"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "primary_palette" in data
        assert "variations" in data

    @pytest.mark.asyncio
    async def test_recommend_colors_by_mood(self, client):
        """Test color recommendation by mood"""
        response = await client.post(
            "/api/v1/aesthetic/colors/recommend",
            json={
                "mood": "calm"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True

    @pytest.mark.asyncio
    async def test_get_color_palettes(self, client):
        """Test getting all color palettes"""
        response = await client.get("/api/v1/aesthetic/palettes")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "palettes" in data
        assert "modern" in data["palettes"]
        assert "minimal" in data["palettes"]


class TestStyleAnalysis:
    """Style analysis endpoint tests"""

    @pytest.mark.asyncio
    async def test_analyze_style(self, client):
        """Test style analysis"""
        response = await client.post(
            "/api/v1/aesthetic/style/analyze",
            json={
                "description": "A modern minimalist design with clean lines and plenty of whitespace"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "primary_style" in data
        assert "detected_styles" in data

    @pytest.mark.asyncio
    async def test_get_styles(self, client):
        """Test getting available styles"""
        response = await client.get("/api/v1/aesthetic/styles")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "styles" in data


class TestAestheticScore:
    """Aesthetic scoring endpoint tests"""

    @pytest.mark.asyncio
    async def test_calculate_aesthetic_score(self, client):
        """Test aesthetic score calculation"""
        response = await client.post(
            "/api/v1/aesthetic/score",
            json={
                "description": "A beautiful modern design",
                "has_gradient": True,
                "has_good_spacing": True,
                "has_good_contrast": True
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "total_score" in data
        assert "grade" in data
        assert "suggestions" in data

    @pytest.mark.asyncio
    async def test_get_moods(self, client):
        """Test getting available moods"""
        response = await client.get("/api/v1/aesthetic/moods")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "moods" in data
