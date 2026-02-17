"""
Image Generation Service
图像生成服务 - 支持Hero Banner、Icon、背景纹理等
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
from PIL import Image
import io
from loguru import logger
from services.ai_models import get_image_generator, get_clip_model, get_clip_preprocess
import torch


class ImageGenerationService:
    """图像生成服务"""

    # 风格预设配置
    STYLE_PRESETS = {
        "modern": {
            "prompt_additions": "modern design, clean lines, minimalist, professional, high quality",
            "negative_prompt": "blurry, low quality, distorted, messy"
        },
        "minimal": {
            "prompt_additions": "minimalist, plenty of whitespace, simple geometry, elegant",
            "negative_prompt": "cluttered, busy, complex, messy"
        },
        "glassmorphism": {
            "prompt_additions": "glass effect, blur, translucent, gradient background, frosted glass",
            "negative_prompt": "opaque, solid colors, flat"
        },
        "neumorphism": {
            "prompt_additions": "soft shadows, extruded shapes, monochromatic, soft UI",
            "negative_prompt": "flat, 2D, no depth"
        },
        "brutalism": {
            "prompt_additions": "bold colors, raw aesthetic, large typography, brutalist design",
            "negative_prompt": "soft, rounded, minimalist"
        },
        "gradient": {
            "prompt_additions": "beautiful gradient, smooth color transitions, vibrant colors",
            "negative_prompt": "solid colors, monochrome"
        },
        "abstract": {
            "prompt_additions": "abstract art, geometric shapes, artistic, creative",
            "negative_prompt": "realistic, photographic, literal"
        }
    }

    # 尺寸预设
    SIZE_PRESETS = {
        "hero_large": (1920, 1080),
        "hero_medium": (1280, 720),
        "hero_small": (1024, 576),
        "icon": (512, 512),
        "banner": (1600, 400),
        "card": (400, 300),
        "thumbnail": (256, 256)
    }

    def __init__(self):
        self.generator = get_image_generator()
        self.clip_model = get_clip_model()
        self.clip_preprocess = get_clip_preprocess()

    def generate_hero_banner(
        self,
        prompt: str,
        style: str = "modern",
        size: str = "hero_medium",
        negative_prompt: Optional[str] = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        生成Hero Banner

        Args:
            prompt: 基础提示词
            style: 风格预设
            size: 尺寸预设
            negative_prompt: 负面提示词
            guidance_scale: 引导强度
            num_inference_steps: 推理步数
            seed: 随机种子
        """
        try:
            if not self.generator:
                raise RuntimeError("Image generator not loaded")

            # 获取风格配置
            style_config = self.STYLE_PRESETS.get(style, self.STYLE_PRESETS["modern"])

            # 构建完整提示词
            full_prompt = f"{prompt}, {style_config['prompt_additions']}, 8k, ultra detailed, masterpiece"
            full_negative = negative_prompt or style_config['negative_prompt']

            # 获取尺寸
            width, height = self.SIZE_PRESETS.get(size, self.SIZE_PRESETS["hero_medium"])

            logger.info(f"Generating hero banner: {prompt[:50]}... | Style: {style} | Size: {width}x{height}")

            # 生成图像
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.generator.device).manual_seed(seed)

            result = self.generator(
                prompt=full_prompt,
                negative_prompt=full_negative,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                generator=generator
            )

            image = result.images[0]

            # 转换为bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()

            # 计算CLIP美学分数
            aesthetic_score = self._calculate_aesthetic_score(image) if self.clip_model else None

            logger.info(f"✅ Hero banner generated | Size: {len(img_bytes)} bytes | Aesthetic: {aesthetic_score}")

            return {
                "image_data": img_bytes,
                "width": width,
                "height": height,
                "format": "PNG",
                "aesthetic_score": aesthetic_score,
                "prompt": full_prompt,
                "seed": seed
            }

        except Exception as e:
            logger.error(f"Failed to generate hero banner: {e}")
            raise

    def generate_icon(
        self,
        concept: str,
        style: str = "outline",
        count: int = 1,
        size: str = "icon",
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        生成Icon

        Args:
            concept: 图标概念描述
            style: 图标风格 (outline, filled, lineart, minimal, 3d)
            count: 生成数量
            size: 尺寸
            seed: 随机种子
        """
        icons = []

        try:
            width, height = self.SIZE_PRESETS.get(size, self.SIZE_PRESETS["icon"])

            # Icon特定风格提示词
            style_prompts = {
                "outline": "icon, outline style, simple lines, vector, transparent background",
                "filled": "icon, filled style, solid shapes, vector, transparent background",
                "lineart": "icon, line art, minimalist, clean lines, transparent background",
                "minimal": "icon, minimal, geometric, simple, transparent background",
                "3d": "icon, 3d rendered, soft shadows, modern, transparent background"
            }

            style_prompt = style_prompts.get(style, style_prompts["outline"])

            for i in range(count):
                full_prompt = f"{concept} icon, {style_prompt}, professional design, high quality"

                logger.info(f"Generating icon {i+1}/{count}: {concept}")

                generator = None
                if seed is not None:
                    current_seed = seed + i
                    generator = torch.Generator(device=self.generator.device).manual_seed(current_seed)

                result = self.generator(
                    prompt=full_prompt,
                    negative_prompt="complex, detailed, photograph, realistic",
                    width=width,
                    height=height,
                    guidance_scale=8.0,
                    num_inference_steps=30,
                    generator=generator
                )

                image = result.images[0]

                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()

                icons.append({
                    "image_data": img_bytes,
                    "concept": concept,
                    "style": style,
                    "variant": i + 1,
                    "width": width,
                    "height": height,
                    "format": "PNG"
                })

            logger.info(f"✅ Generated {len(icons)} icons")
            return icons

        except Exception as e:
            logger.error(f"Failed to generate icons: {e}")
            raise

    def generate_background(
        self,
        style: str = "gradient",
        colors: Optional[List[str]] = None,
        complexity: str = "medium",
        size: str = "hero_medium",
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        生成背景纹理

        Args:
            style: 背景风格 (gradient, pattern, abstract, mesh, noise)
            colors: 颜色列表
            complexity: 复杂度 (low, medium, high)
            size: 尺寸
            seed: 随机种子
        """
        try:
            # 构建颜色提示词
            if colors:
                color_prompt = f"colors: {', '.join(colors)}"
            else:
                color_prompt = "vibrant, modern colors"

            # 风格提示词
            style_prompts = {
                "gradient": f"beautiful gradient, smooth color transitions, {color_prompt}, modern",
                "pattern": f"geometric pattern, {color_prompt}, subtle, professional background",
                "abstract": f"abstract background, artistic, {color_prompt}, subtle texture",
                "mesh": f"mesh gradient, {color_prompt}, smooth, modern, elegant",
                "noise": f"subtle noise texture, {color_prompt}, professional background"
            }

            # 复杂度控制
            complexity_prompts = {
                "low": "simple, minimal",
                "medium": "balanced, elegant",
                "high": "complex, detailed, intricate"
            }

            full_prompt = f"{style_prompts.get(style, style_prompts['gradient'])}, {complexity_prompts.get(complexity, 'balanced')}"

            width, height = self.SIZE_PRESETS.get(size, self.SIZE_PRESETS["hero_medium"])

            logger.info(f"Generating background: {style} | Complexity: {complexity}")

            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.generator.device).manual_seed(seed)

            result = self.generator(
                prompt=full_prompt,
                negative_prompt="distracting, busy, overwhelming, photo, realistic",
                width=width,
                height=height,
                guidance_scale=6.0,
                num_inference_steps=40,
                generator=generator
            )

            image = result.images[0]

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()

            logger.info(f"✅ Background generated | Style: {style}")
            return {
                "image_data": img_bytes,
                "style": style,
                "colors": colors,
                "complexity": complexity,
                "width": width,
                "height": height,
                "format": "PNG"
            }

        except Exception as e:
            logger.error(f"Failed to generate background: {e}")
            raise

    def _calculate_aesthetic_score(self, image: Image.Image) -> float:
        """
        使用CLIP计算美学分数

        Args:
            image: PIL图像

        Returns:
            美学分数 (0-1)
        """
        try:
            if not self.clip_model or not self.clip_preprocess:
                return 0.5

            # 预处理图像
            image_input = self.clip_preprocess(image).unsqueeze(0)

            # 获取图像特征
            with torch.no_grad():
                image_features = self.clip_model.encode_image(image_input)

            # 简单美学评估（基于特征范数）
            score = float(torch.norm(image_features).item())
            normalized_score = min(max(score / 10.0, 0.0), 1.0)

            return normalized_score

        except Exception as e:
            logger.warning(f"Failed to calculate aesthetic score: {e}")
            return 0.5


# 全局服务实例
image_service = ImageGenerationService()
