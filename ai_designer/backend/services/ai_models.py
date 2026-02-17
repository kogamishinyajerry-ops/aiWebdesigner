"""
AI Models Service
管理所有AI模型的加载、推理和生命周期
"""

import os
from typing import Optional, Dict, Any
from loguru import logger
import torch
from pathlib import Path

# Import AI frameworks
try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False
    logger.warning("diffusers not available - image generation disabled")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not available - Gemini API disabled")

try:
    import clip
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False
    logger.warning("clip not available - CLIP features disabled")


class ModelManager:
    """AI模型管理器 - 单例模式"""

    _instance: Optional['ModelManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.device = self._get_device()
            self.models: Dict[str, Any] = {}
            self._initialized = True
            logger.info(f"ModelManager initialized with device: {self.device}")

    @staticmethod
    def _get_device() -> str:
        """获取可用设备"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    async def load_all_models(self) -> Dict[str, bool]:
        """加载所有AI模型"""
        logger.info("Loading AI models...")
        results = {}

        # 1. 加载图像生成模型 (FLUX/SDXL)
        results["image_generator"] = await self.load_image_generator()

        # 2. 加载Gemini API客户端
        results["gemini"] = await self.load_gemini_client()

        # 3. 加载CLIP模型
        results["clip"] = await self.load_clip_model()

        summary = {k: "✅" if v else "❌" for k, v in results.items()}
        logger.info(f"Model loading complete: {summary}")

        return results

    async def load_image_generator(self) -> bool:
        """加载图像生成模型 (FLUX.1 或 SDXL)"""
        try:
            if not DIFFUSERS_AVAILABLE:
                logger.warning("Diffusers not available, skipping image generator")
                return False

            model_id = os.getenv(
                "IMAGE_MODEL_ID",
                "stabilityai/stable-diffusion-xl-base-1.0"
            )

            logger.info(f"Loading image generation model: {model_id}")

            # 使用float16节省显存
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                use_safetensors=True
            )

            # 使用DPM++调度器提高速度
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

            # 移动到设备
            pipe = pipe.to(self.device)

            # 启用内存优化
            if self.device == "cuda":
                pipe.enable_attention_slicing()
                pipe.enable_vae_slicing()

            self.models["image_generator"] = pipe
            logger.info("✅ Image generation model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load image generator: {e}")
            return False

    async def load_gemini_client(self) -> bool:
        """加载Gemini API客户端"""
        try:
            if not GEMINI_AVAILABLE:
                logger.warning("google-generativeai not available, skipping Gemini")
                return False

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("GEMINI_API_KEY not set, Gemini API disabled")
                return False

            genai.configure(api_key=api_key)
            self.models["gemini_client"] = genai

            # 配置模型
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
            model = genai.GenerativeModel(model_name)

            self.models["gemini_model"] = model
            logger.info("✅ Gemini API client initialized")
            return True

        except Exception as e:
            logger.error(f"Failed to load Gemini client: {e}")
            return False

    async def load_clip_model(self) -> bool:
        """加载CLIP模型用于视觉理解"""
        try:
            if not CLIP_AVAILABLE:
                logger.warning("clip not available, skipping CLIP")
                return False

            logger.info("Loading CLIP model...")

            device = self.device if self.device != "mps" else "cpu"  # CLIP不完全支持MPS
            model, preprocess = clip.load("ViT-B/32", device=device)

            self.models["clip_model"] = model
            self.models["clip_preprocess"] = preprocess

            logger.info("✅ CLIP model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            return False

    def get_model(self, model_name: str) -> Optional[Any]:
        """获取已加载的模型"""
        return self.models.get(model_name)

    def is_loaded(self, model_name: str) -> bool:
        """检查模型是否已加载"""
        return model_name in self.models

    async def unload_model(self, model_name: str) -> bool:
        """卸载指定模型释放内存"""
        try:
            if model_name in self.models:
                model = self.models[model_name]

                # 清理GPU内存
                if hasattr(model, 'to'):
                    model.to("cpu")

                del self.models[model_name]
                torch.cuda.empty_cache() if self.device == "cuda" else None

                logger.info(f"✅ Model {model_name} unloaded")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to unload model {model_name}: {e}")
            return False

    async def unload_all(self):
        """卸载所有模型"""
        for model_name in list(self.models.keys()):
            await self.unload_model(model_name)


# 全局模型管理器实例
model_manager = ModelManager()


# 便捷访问函数
def get_image_generator():
    """获取图像生成模型"""
    return model_manager.get_model("image_generator")


def get_gemini_client():
    """获取Gemini API客户端"""
    return model_manager.get_model("gemini_client")


def get_gemini_model():
    """获取Gemini模型实例"""
    return model_manager.get_model("gemini_model")


def get_clip_model():
    """获取CLIP模型"""
    return model_manager.get_model("clip_model")


def get_clip_preprocess():
    """获取CLIP预处理函数"""
    return model_manager.get_model("clip_preprocess")
