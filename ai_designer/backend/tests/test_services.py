"""
Test Services
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from PIL import Image
import torch


class TestImageService:
    """Image generation service tests"""

    @pytest.mark.asyncio
    async def test_generate_hero_banner_no_model(self):
        """Test hero banner generation without model"""
        from services.image_generation import ImageGenerationService

        service = ImageGenerationService()
        service.generator = None

        with pytest.raises(RuntimeError):
            service.generate_hero_banner(
                prompt="Test prompt",
                style="modern"
            )

    @pytest.mark.asyncio
    async def test_style_presets_exist(self):
        """Test that style presets are defined"""
        from services.image_generation import ImageGenerationService

        service = ImageGenerationService()
        assert "modern" in service.STYLE_PRESETS
        assert "minimal" in service.STYLE_PRESETS
        assert "glassmorphism" in service.STYLE_PRESETS

    @pytest.mark.asyncio
    async def test_size_presets_exist(self):
        """Test that size presets are defined"""
        from services.image_generation import ImageGenerationService

        service = ImageGenerationService()
        assert "hero_large" in service.SIZE_PRESETS
        assert "hero_medium" in service.SIZE_PRESETS
        assert "icon" in service.SIZE_PRESETS


class TestSVGService:
    """SVG generation service tests"""

    @pytest.mark.asyncio
    async def test_text_to_svg_template_fallback(self):
        """Test SVG generation with template fallback"""
        from services.svgn_generation import SVGGenerationService

        service = SVGGenerationService()
        service.gemini_model = None

        result = await service.text_to_svg(
            description="a circle",
            style="modern",
            width=512,
            height=512
        )

        assert result["svg_code"] is not None
        assert "<svg" in result["svg_code"]
        assert result["width"] == 512
        assert result["height"] == 512

    @pytest.mark.asyncio
    async def test_parse_description(self):
        """Test description parsing"""
        from services.svgn_generation import SVGGenerationService

        service = SVGGenerationService()
        elements = service._parse_description("a circle and triangle")

        assert len(elements) > 0
        assert any(e["type"] == "circle" for e in elements)


class TestCodeService:
    """Code generation service tests"""

    @pytest.mark.asyncio
    async def test_design_to_code_template_fallback(self):
        """Test code generation with template fallback"""
        from services.code_generation import CodeGenerationService

        service = CodeGenerationService()
        service.gemini_model = None

        result = await service.design_to_code(
            description="A simple button",
            framework="react",
            language="typescript"
        )

        assert result["code"] is not None
        assert result["framework"] == "react"
        assert "React" in result["code"]

    @pytest.mark.asyncio
    async def test_parse_description_keywords(self):
        """Test keyword extraction from description"""
        from services.code_generation import CodeGenerationService

        service = CodeGenerationService()
        keywords = service._parse_description("A card component with gradient and dark mode")

        assert "card" in keywords
        assert "gradient" in keywords
        assert "dark" in keywords


class TestAestheticEngine:
    """Aesthetic engine tests"""

    @pytest.mark.asyncio
    async def test_recommend_colors(self):
        """Test color recommendation"""
        from services.aesthetic_engine import AestheticEngine

        engine = AestheticEngine()
        result = engine.recommend_colors(style="modern")

        assert "primary_palette" in result
        assert "variations" in result
        assert result["primary_palette"]["name"] == "Modern Purple"

    @pytest.mark.asyncio
    async def test_analyze_style(self):
        """Test style analysis"""
        from services.aesthetic_engine import AestheticEngine

        engine = AestheticEngine()
        result = engine.analyze_style("A modern minimalist design")

        assert "primary_style" in result
        assert "detected_styles" in result

    @pytest.mark.asyncio
    async def test_calculate_aesthetic_score(self):
        """Test aesthetic scoring"""
        from services.aesthetic_engine import AestheticEngine

        engine = AestheticEngine()
        result = engine.calculate_aesthetic_score(
            description="Beautiful design",
            has_gradient=True,
            has_good_spacing=True,
            has_good_contrast=True
        )

        assert "total_score" in result
        assert "grade" in result
        assert 0 <= result["total_score"] <= 1

    @pytest.mark.asyncio
    async def test_get_aesthetic_grade(self):
        """Test grade assignment"""
        from services.aesthetic_engine import AestheticEngine

        engine = AestheticEngine()

        assert engine._get_aesthetic_grade(0.95) == "A+"
        assert engine._get_aesthetic_grade(0.85) == "A"
        assert engine._get_aesthetic_grade(0.75) == "B+"
        assert engine._get_aesthetic_grade(0.65) == "B"
        assert engine._get_aesthetic_grade(0.55) == "C"
        assert engine._get_aesthetic_grade(0.45) == "D"


class TestModelManager:
    """Model manager tests"""

    @pytest.mark.asyncio
    async def test_get_device(self):
        """Test device detection"""
        from services.ai_models import ModelManager

        manager = ModelManager()
        device = manager._get_device()
        assert device in ["cuda", "mps", "cpu"]

    @pytest.mark.asyncio
    async def test_is_loaded_empty(self):
        """Test that no models are loaded initially"""
        from services.ai_models import ModelManager

        manager = ModelManager()
        assert manager.is_loaded("image_generator") is False
