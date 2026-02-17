"""
Image Generation Service
使用FLUX模型进行图像生成
"""

import torch
from diffusers import FluxPipeline
from PIL import Image
import io
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import uuid
from loguru import logger

from core.config import settings


class ImageGenerator:
    """图像生成器"""
    
    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.upload_dir = Path(settings.UPLOAD_DIR) / "images"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
    async def load_model(self):
        """加载FLUX模型"""
        if self.pipeline is not None:
            return
        
        logger.info(f"Loading FLUX model on {self.device}...")
        
        try:
            self.pipeline = FluxPipeline.from_pretrained(
                settings.FLUX_MODEL_PATH,
                torch_dtype=self.dtype,
                use_safetensors=True
            )
            self.pipeline.to(self.device)
            self.pipeline.enable_model_cpu_offload()
            logger.info("✅ FLUX model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load FLUX model: {e}")
            raise
    
    def _build_style_prompt(self, style: str) -> str:
        """构建风格prompt"""
        style_prompts = {
            "modern": "clean design, flat colors, modern typography, sans-serif, professional",
            "minimal": "minimalist, plenty of whitespace, simple geometry, elegant, clean",
            "glassmorphism": "glass effect, blur, translucent, gradient background, modern UI",
            "neumorphism": "soft shadows, extruded shapes, monochromatic, soft UI",
            "brutalism": "bold colors, raw aesthetic, large typography, bold design"
        }
        return style_prompts.get(style, "clean design, modern, professional")
    
    async def generate(
        self,
        prompt: str,
        style: str = "modern",
        width: int = 1920,
        height: int = 1080,
        num_images: int = 1,
        seed: Optional[int] = None
    ) -> List[Image.Image]:
        """
        生成图像
        
        Args:
            prompt: 描述文本
            style: 风格预设
            width: 宽度
            height: 高度
            num_images: 生成数量
            seed: 随机种子
        
        Returns:
            生成的图像列表
        """
        if self.pipeline is None:
            await self.load_model()
        
        # 构建完整prompt
        style_prompt = self._build_style_prompt(style)
        full_prompt = f"{prompt}, {style_prompt}, high quality, 8k, professional"
        
        logger.info(f"Generating image with prompt: {prompt[:50]}...")
        
        try:
            # 设置随机种子
            generator = None
            if seed is not None:
                generator = torch.Generator(self.device).manual_seed(seed)
            
            # 生成图像
            with torch.no_grad():
                images = self.pipeline(
                    prompt=full_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=50,
                    guidance_scale=7.5,
                    num_images_per_prompt=num_images,
                    generator=generator
                ).images
            
            logger.info(f"✅ Generated {len(images)} images")
            return images
            
        except Exception as e:
            logger.error(f"❌ Failed to generate images: {e}")
            raise
    
    async def generate_hero_banner(
        self,
        prompt: str,
        style: str,
        width: int,
        height: int,
        title: Optional[str] = None
    ) -> List[Image.Image]:
        """
        生成Hero Banner
        
        Args:
            prompt: 描述文本
            style: 风格
            width: 宽度
            height: 高度
            title: 标题文本
        
        Returns:
            生成的图像列表
        """
        # 添加web设计相关的描述
        web_prompt = f"{prompt}, website hero banner, professional web design, {style} style"
        
        images = await self.generate(
            prompt=web_prompt,
            style=style,
            width=width,
            height=height,
            num_images=1
        )
        
        # 后处理
        processed_images = []
        for image in images:
            processed = self._enhance_for_web(image, title)
            processed_images.append(processed)
        
        return processed_images
    
    def _enhance_for_web(self, image: Image.Image, title: Optional[str] = None) -> Image.Image:
        """Web优化处理"""
        # 如果有标题，可以添加文字叠加
        # 这里只是简单示例
        return image
    
    async def save_image(self, image: Image.Image, image_id: str) -> str:
        """
        保存图像
        
        Args:
            image: PIL图像
            image_id: 图像ID
        
        Returns:
            图像URL
        """
        # 生成文件名
        filename = f"{image_id}.png"
        filepath = self.upload_dir / filename
        
        # 保存图像
        image.save(filepath, format="PNG", quality=95)
        
        # 返回URL
        return f"/api/v1/image/{image_id}"
    
    async def get_image(self, image_id: str) -> Image.Image:
        """
        获取图像
        
        Args:
            image_id: 图像ID
        
        Returns:
            PIL图像
        """
        filepath = self.upload_dir / f"{image_id}.png"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Image {image_id} not found")
        
        return Image.open(filepath)


# Global instance
image_generator = ImageGenerator()
