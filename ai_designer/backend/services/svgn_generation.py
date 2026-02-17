"""
SVG Generation Service
SVG生成服务 - Text to SVG, Icon批量生成等
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import json
from loguru import logger
from services.ai_models import get_gemini_model


@dataclass
class SVGElement:
    """SVG元素基类"""
    tag: str
    attributes: Dict[str, str]
    children: Optional[List['SVGElement']] = None

    def to_xml(self) -> str:
        """转换为XML"""
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        if self.children:
            children_xml = "\n    ".join([child.to_xml() for child in self.children])
            return f"<{self.tag} {attrs}>\n    {children_xml}\n  </{self.tag}>"
        else:
            return f"<{self.tag} {attrs} />"


class SVGGenerationService:
    """SVG生成服务"""

    def __init__(self):
        self.gemini_model = get_gemini_model()

    async def text_to_svg(
        self,
        description: str,
        style: str = "modern",
        width: int = 512,
        height: int = 512,
        optimize: bool = True
    ) -> Dict[str, Any]:
        """
        文本描述生成SVG

        Args:
            description: 文本描述 (如 "a minimalist logo with a circle and triangle")
            style: 设计风格
            width: 宽度
            height: 高度
            optimize: 是否优化SVG代码

        Returns:
            SVG代码和元数据
        """
        try:
            logger.info(f"Generating SVG from description: {description}")

            if self.gemini_model:
                svg_code = await self._generate_with_gemini(description, style, width, height)
            else:
                # 回退到模板生成
                svg_code = self._generate_from_template(description, style, width, height)

            if optimize:
                svg_code = self._optimize_svg(svg_code)

            # 提取元数据
            metadata = self._extract_svg_metadata(svg_code)

            logger.info("✅ SVG generated successfully")
            return {
                "svg_code": svg_code,
                "width": width,
                "height": height,
                "style": style,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Failed to generate SVG: {e}")
            raise

    async def _generate_with_gemini(
        self,
        description: str,
        style: str,
        width: int,
        height: int
    ) -> str:
        """使用Gemini生成SVG"""
        try:
            prompt = f"""Generate SVG code for: {description}

Style: {style}
Size: {width}x{height}

Requirements:
- Clean, efficient SVG code
- Proper viewBox
- Semantic structure
- Inline styles preferred
- No external dependencies

Return ONLY the SVG code, no explanations.
"""

            response = self.gemini_model.generate_content(prompt)
            svg_text = response.text

            # 提取SVG代码
            if "<svg" in svg_text:
                # 提取第一个SVG标签到结束标签
                start = svg_text.find("<svg")
                end = svg_text.rfind("</svg>") + 6
                return svg_text[start:end]
            else:
                raise ValueError("No SVG code found in response")

        except Exception as e:
            logger.error(f"Gemini SVG generation failed: {e}")
            raise

    def _generate_from_template(
        self,
        description: str,
        style: str,
        width: int,
        height: int
    ) -> str:
        """从模板生成SVG（回退方案）"""
        logger.info("Using template-based SVG generation")

        # 解析描述中的元素
        elements = self._parse_description(description)

        # 构建SVG
        svg_elements = []

        # 添加背景（可选）
        if style == "glassmorphism":
            svg_elements.append(SVGElement("rect", {
                "x": "0", "y": "0", "width": str(width), "height": str(height),
                "fill": "rgba(255, 255, 255, 0.1)",
                "filter": "drop-shadow(0 4px 6px rgba(0,0,0,0.1))"
            }))

        # 添加识别到的元素
        for elem in elements:
            if elem["type"] == "circle":
                svg_elements.append(SVGElement("circle", {
                    "cx": str(elem.get("x", width // 2)),
                    "cy": str(elem.get("y", height // 2)),
                    "r": str(elem.get("size", 50)),
                    "fill": self._get_color(style, elem.get("color", "primary"))
                }))
            elif elem["type"] == "triangle":
                points = self._triangle_points(
                    elem.get("x", width // 2),
                    elem.get("y", height // 2),
                    elem.get("size", 50)
                )
                svg_elements.append(SVGElement("polygon", {
                    "points": points,
                    "fill": self._get_color(style, elem.get("color", "secondary"))
                }))
            elif elem["type"] == "rectangle":
                svg_elements.append(SVGElement("rect", {
                    "x": str(elem.get("x", width // 2 - 50)),
                    "y": str(elem.get("y", height // 2 - 50)),
                    "width": str(elem.get("width", 100)),
                    "height": str(elem.get("height", 100)),
                    "fill": self._get_color(style, elem.get("color", "accent"))
                }))

        # 组装SVG
        elements_xml = "\n    ".join([elem.to_xml() for elem in svg_elements])

        svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  {elements_xml}
</svg>"""

        return svg_code

    def _parse_description(self, description: str) -> List[Dict[str, Any]]:
        """解析描述提取元素"""
        elements = []
        desc_lower = description.lower()

        # 简单的关键词匹配
        if "circle" in desc_lower:
            elements.append({"type": "circle", "x": None, "y": None, "size": 50, "color": "primary"})
        if "triangle" in desc_lower:
            elements.append({"type": "triangle", "x": None, "y": None, "size": 50, "color": "secondary"})
        if "rectangle" in desc_lower or "rect" in desc_lower:
            elements.append({"type": "rectangle", "x": None, "y": None, "width": 100, "height": 100, "color": "accent"})

        # 如果没有识别到元素，添加一个默认圆
        if not elements:
            elements.append({"type": "circle", "x": None, "y": None, "size": 60, "color": "primary"})

        return elements

    def _triangle_points(self, cx: int, cy: int, size: int) -> str:
        """计算三角形顶点"""
        points = [
            (cx, cy - size),
            (cx - size, cy + size),
            (cx + size, cy + size)
        ]
        return ",".join([f"{x},{y}" for x, y in points])

    def _get_color(self, style: str, color_type: str) -> str:
        """获取颜色"""
        color_palettes = {
            "modern": {
                "primary": "#6366f1",
                "secondary": "#8b5cf6",
                "accent": "#f59e0b"
            },
            "minimal": {
                "primary": "#1f2937",
                "secondary": "#4b5563",
                "accent": "#3b82f6"
            },
            "gradient": {
                "primary": "url(#gradient1)",
                "secondary": "url(#gradient2)",
                "accent": "url(#gradient3)"
            }
        }

        palette = color_palettes.get(style, color_palettes["modern"])
        return palette.get(color_type, "#6366f1")

    def _optimize_svg(self, svg_code: str) -> str:
        """优化SVG代码"""
        # 移除多余空格
        svg_code = " ".join(svg_code.split())

        # 移除不必要的属性
        # (简化处理，实际可以使用svgo等工具)

        return svg_code

    def _extract_svg_metadata(self, svg_code: str) -> Dict[str, Any]:
        """提取SVG元数据"""
        metadata = {
            "element_count": svg_code.count("<") - svg_code.count("</svg>") - svg_code.count("<svg"),
            "has_gradient": "gradient" in svg_code.lower(),
            "has_animation": "<animate" in svg_code,
            "estimated_size": len(svg_code.encode('utf-8'))
        }
        return metadata

    async def generate_icon_set(
        self,
        concept: str,
        count: int = 10,
        style: str = "outline",
        size: int = 512
    ) -> List[Dict[str, Any]]:
        """
        批量生成Icon集

        Args:
            concept: 图标概念 (如 "navigation", "social", "e-commerce")
            count: 数量
            style: 风格
            size: 尺寸

        Returns:
            图标列表
        """
        icons = []

        # 图标概念映射
        icon_concepts = {
            "navigation": ["home", "menu", "arrow-left", "arrow-right", "search", "settings", "user", "bell", "heart", "bookmark"],
            "social": ["facebook", "twitter", "instagram", "linkedin", "youtube", "github", "telegram", "whatsapp", "tiktok", "discord"],
            "e-commerce": ["cart", "bag", "credit-card", "tag", "truck", "store", "wishlist", "coupon", "package", "receipt"],
            "media": ["play", "pause", "stop", "volume", "mute", "fullscreen", "skip-next", "skip-prev", "repeat", "shuffle"],
            "files": ["file", "folder", "document", "image", "video", "audio", "archive", "cloud", "upload", "download"],
            "charts": ["chart-line", "chart-bar", "chart-pie", "chart-area", "trend-up", "trend-down", "analytics", "statistics", "growth", "decline"]
        }

        concept_list = icon_concepts.get(concept, [f"{concept}_{i}" for i in range(count)])

        for i, icon_name in enumerate(concept_list[:count]):
            description = f"a {style} icon for {icon_name}"
            result = await self.text_to_svg(description, style, size, size)
            result["name"] = icon_name
            result["index"] = i + 1
            icons.append(result)

        logger.info(f"✅ Generated {len(icons)} icons for {concept}")
        return icons


# 全局服务实例
svg_service = SVGGenerationService()
