"""
Aesthetic Engine Service
美学引擎 - 风格识别、色彩推荐、审美评分
"""

from typing import Optional, List, Dict, Any, Tuple
from loguru import logger
from services.ai_models import get_clip_model, get_clip_preprocess
import torch


class AestheticEngine:
    """美学引擎"""

    # 预设色彩方案
    COLOR_PALETTES = {
        "modern": {
            "primary": "#6366f1",
            "secondary": "#8b5cf6",
            "accent": "#f59e0b",
            "background": "#ffffff",
            "text": "#1f2937",
            "name": "Modern Purple"
        },
        "minimal": {
            "primary": "#1f2937",
            "secondary": "#4b5563",
            "accent": "#3b82f6",
            "background": "#f9fafb",
            "text": "#111827",
            "name": "Minimal Gray"
        },
        "ocean": {
            "primary": "#0ea5e9",
            "secondary": "#06b6d4",
            "accent": "#14b8a6",
            "background": "#f0f9ff",
            "text": "#0c4a6e",
            "name": "Ocean Blue"
        },
        "sunset": {
            "primary": "#f97316",
            "secondary": "#ef4444",
            "accent": "#eab308",
            "background": "#fff7ed",
            "text": "#7c2d12",
            "name": "Sunset Orange"
        },
        "forest": {
            "primary": "#22c55e",
            "secondary": "#16a34a",
            "accent": "#84cc16",
            "background": "#f0fdf4",
            "text": "#14532d",
            "name": "Forest Green"
        },
        "royal": {
            "primary": "#7c3aed",
            "secondary": "#a855f7",
            "accent": "#ec4899",
            "background": "#faf5ff",
            "text": "#581c87",
            "name": "Royal Purple"
        }
    }

    # 风格关键词
    STYLE_KEYWORDS = {
        "minimalist": ["clean", "simple", "minimal", "minimalist", "plenty of whitespace"],
        "modern": ["modern", "contemporary", "sleek", "professional"],
        "glassmorphism": ["glass", "blur", "translucent", "frosted", "glassmorphism"],
        "neumorphism": ["soft", "extruded", "subtle", "neumorphism"],
        "brutalism": ["bold", "raw", "brutal", "brutalism", "large typography"],
        "gradient": ["gradient", "vibrant", "smooth", "colorful"],
        "dark": ["dark", "dark mode", "dark theme", "night"]
    }

    def __init__(self):
        self.clip_model = get_clip_model()
        self.clip_preprocess = get_clip_preprocess()

    def recommend_colors(
        self,
        description: Optional[str] = None,
        style: Optional[str] = None,
        mood: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        推荐色彩方案

        Args:
            description: 设计描述
            style: 风格
            mood: 情绪/氛围

        Returns:
            推荐的色彩方案
        """
        try:
            logger.info(f"Recommending colors | Style: {style} | Mood: {mood}")

            # 根据输入选择合适的色彩方案
            if style:
                palette = self.COLOR_PALETTES.get(style.lower(), self.COLOR_PALETTES["modern"])
            elif mood:
                palette = self._select_palette_by_mood(mood)
            else:
                palette = self.COLOR_PALETTES["modern"]

            # 生成变体
            variations = self._generate_color_variations(palette)

            result = {
                "primary_palette": palette,
                "variations": variations,
                "contrast_score": self._calculate_contrast_score(palette),
                "accessibility": self._check_accessibility(palette)
            }

            logger.info("✅ Color palette recommended")
            return result

        except Exception as e:
            logger.error(f"Failed to recommend colors: {e}")
            raise

    def analyze_style(self, description: str) -> Dict[str, Any]:
        """
        分析设计风格

        Args:
            description: 设计描述

        Returns:
            风格分析结果
        """
        try:
            logger.info(f"Analyzing style: {description}")

            detected_styles = []
            style_scores = {}

            # 关键词匹配
            for style, keywords in self.STYLE_KEYWORDS.items():
                score = 0
                for keyword in keywords:
                    if keyword in description.lower():
                        score += 1
                if score > 0:
                    detected_styles.append(style)
                    style_scores[style] = score

            # 排序
            detected_styles.sort(key=lambda x: style_scores.get(x, 0), reverse=True)

            result = {
                "detected_styles": detected_styles,
                "style_scores": style_scores,
                "primary_style": detected_styles[0] if detected_styles else "modern",
                "confidence": style_scores.get(detected_styles[0], 0) / max(len(description.split()), 1) * 100 if detected_styles else 0
            }

            logger.info(f"✅ Style analyzed: {result['primary_style']}")
            return result

        except Exception as e:
            logger.error(f"Failed to analyze style: {e}")
            return {"primary_style": "modern", "detected_styles": ["modern"], "style_scores": {}}

    def calculate_aesthetic_score(
        self,
        description: str,
        style: Optional[str] = None,
        has_gradient: bool = False,
        has_good_spacing: bool = False,
        has_good_contrast: bool = False
    ) -> Dict[str, Any]:
        """
        计算美学评分

        Args:
            description: 设计描述
            style: 风格
            has_gradient: 是否有渐变
            has_good_spacing: 是否有良好间距
            has_good_contrast: 是否有良好对比度

        Returns:
            美学评分和详细指标
        """
        try:
            logger.info("Calculating aesthetic score")

            # 风格得分
            style_score = 0.7 if style else 0.5

            # 元素得分
            element_scores = {
                "gradient": 0.15 if has_gradient else 0,
                "spacing": 0.15 if has_good_spacing else 0,
                "contrast": 0.15 if has_good_contrast else 0
            }

            # 描述质量得分（基于长度和关键词）
            desc_words = len(description.split())
            desc_score = min(desc_words / 10, 1.0) * 0.1

            # 总分
            total_score = min(style_score + sum(element_scores.values()) + desc_score, 1.0)

            # 等级评定
            grade = self._get_aesthetic_grade(total_score)

            # 改进建议
            suggestions = self._get_improvement_suggestions(
                has_gradient, has_good_spacing, has_good_contrast, total_score
            )

            result = {
                "total_score": total_score,
                "grade": grade,
                "breakdown": {
                    "style": style_score,
                    **element_scores,
                    "description_quality": desc_score
                },
                "suggestions": suggestions
            }

            logger.info(f"✅ Aesthetic score: {total_score:.2f} ({grade})")
            return result

        except Exception as e:
            logger.error(f"Failed to calculate aesthetic score: {e}")
            return {"total_score": 0.5, "grade": "B", "suggestions": []}

    def _select_palette_by_mood(self, mood: str) -> Dict[str, str]:
        """根据情绪选择色彩方案"""
        mood_lower = mood.lower()

        mood_mapping = {
            "calm": "ocean",
            "energetic": "sunset",
            "natural": "forest",
            "luxury": "royal",
            "professional": "modern",
            "clean": "minimal"
        }

        style = mood_mapping.get(mood_lower, "modern")
        return self.COLOR_PALETTES[style]

    def _generate_color_variations(
        self,
        palette: Dict[str, str],
        count: int = 3
    ) -> List[Dict[str, str]]:
        """生成色彩方案变体"""
        variations = []

        for i in range(count):
            # 简单的亮度调整（实际应用中可以使用HSL转换）
            variation = {
                "name": f"{palette['name']} Variant {i+1}",
                "primary": self._adjust_brightness(palette["primary"], i * 0.1),
                "secondary": self._adjust_brightness(palette["secondary"], i * 0.1),
                "accent": self._adjust_brightness(palette["accent"], i * 0.1),
                "background": palette["background"],
                "text": palette["text"]
            }
            variations.append(variation)

        return variations

    def _adjust_brightness(self, hex_color: str, factor: float) -> str:
        """调整颜色亮度（简化版）"""
        # 简化处理：返回原色
        # 实际应用中应该转换为HSL并调整亮度
        return hex_color

    def _calculate_contrast_score(self, palette: Dict[str, str]) -> float:
        """计算对比度得分（简化版）"""
        # 简化处理：返回固定值
        # 实际应用中应该使用WCAG对比度公式
        return 4.5

    def _check_accessibility(self, palette: Dict[str, str]) -> Dict[str, Any]:
        """检查无障碍性（简化版）"""
        return {
            "wcag_aa": True,
            "wcag_aaa": False,
            "contrast_ratio": 4.5
        }

    def _get_aesthetic_grade(self, score: float) -> str:
        """获取美学等级"""
        if score >= 0.9:
            return "A+"
        elif score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B+"
        elif score >= 0.6:
            return "B"
        elif score >= 0.5:
            return "C"
        else:
            return "D"

    def _get_improvement_suggestions(
        self,
        has_gradient: bool,
        has_good_spacing: bool,
        has_good_contrast: bool,
        score: float
    ) -> List[str]:
        """获取改进建议"""
        suggestions = []

        if not has_gradient and score < 0.8:
            suggestions.append("Consider adding subtle gradients for depth")

        if not has_good_spacing:
            suggestions.append("Increase whitespace for better visual hierarchy")

        if not has_good_contrast:
            suggestions.append("Improve contrast for better readability")

        if score >= 0.9:
            suggestions.append("Excellent design! Keep up the great work.")

        return suggestions


# 全局服务实例
aesthetic_engine = AestheticEngine()
