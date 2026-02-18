"""
Aesthetic Design Generation Service
美学设计生成服务 - 基于艺术巨匠风格的前端美学方案生成
"""

from typing import Dict, List, Any, Optional
from loguru import logger
import json


class AestheticGenerationService:
    """美学设计生成服务"""

    # 艺术大师风格数据库
    ART_STYLES = {
        "van_gogh": {
            "name": "Vincent van Gogh",
            "description": "后印象派大师，以独特的旋涡笔触和强烈的情感表达著称",
            "key_characteristics": [
                "旋涡状笔触和动态线条",
                "浓郁厚重的色彩堆叠",
                "强烈的情感对比",
                "夜晚与星空主题",
                "金黄与蓝色的经典配色"
            ],
            "color_philosophy": "使用互补色创造强烈对比，金黄色与深蓝色的经典组合，厚涂技法增加色彩深度",
            "compositional_principles": [
                "动态曲线引导视线",
                "色彩对比创造视觉焦点",
                "厚重的笔触增加质感",
                "情感化的构图表达"
            ],
            "mood": "激情、热烈、梦幻、忧郁",
            "suitability": ["艺术展示", "创意产品", "品牌故事", "情感化应用"],
            "primary_colors": ["#F5C518", "#0D1B2A", "#1B4965", "#62B6CB"],
            "typography": "衬线字体，笔触感设计",
            "interaction": "流畅的旋涡动画，色彩渐变过渡"
        },
        "picasso": {
            "name": "Pablo Picasso",
            "description": "立体主义先驱，以几何碎片和多视角构图著称",
            "key_characteristics": [
                "几何碎片化构图",
                "多视角同时呈现",
                "简洁的线条和色块",
                "黑白与鲜明色彩对比",
                "解构与重组的美学"
            ],
            "color_philosophy": "使用几何色块，大胆的黑白对比，限制色板创造视觉冲击力",
            "compositional_principles": [
                "几何形状的解构与重组",
                "多视角的空间表达",
                "负空间的巧妙运用",
                "不对称的平衡构图"
            ],
            "mood": "先锋、现代、前卫、大胆",
            "suitability": ["科技产品", "创意工具", "设计平台", "现代应用"],
            "primary_colors": ["#000000", "#FFFFFF", "#E63946", "#457B9D", "#A8DADC"],
            "typography": "无衬线字体，几何形状",
            "interaction": "几何形状的变换与重组"
        },
        "dali": {
            "name": "Salvador Dalí",
            "description": "超现实主义大师，以梦境般的意象和视错觉著称",
            "key_characteristics": [
                "梦幻般的超现实意象",
                "精确的细节与荒诞的结合",
                "柔和流动的形态",
                "时钟融化的经典元素",
                "无限的视觉延伸"
            ],
            "color_philosophy": "柔和的色彩过渡，透明与半透明效果，梦幻的色调混合",
            "compositional_principles": [
                "流动的形态引导视线",
                "超现实的空间关系",
                "精确细节与荒诞意象对比",
                "无限延伸的视觉错觉"
            ],
            "mood": "神秘、梦幻、超现实、奇幻",
            "suitability": ["创意工具", "艺术应用", "沉浸式体验", "游戏界面"],
            "primary_colors": ["#F4A261", "#2A9D8F", "#E9C46A", "#264653", "#E76F51"],
            "typography": "手写字体，流动感设计",
            "interaction": "流体动画，变形过渡效果"
        },
        "monet": {
            "name": "Claude Monet",
            "description": "印象派之父，以光影色彩和模糊印象著称",
            "key_characteristics": [
                "光影的瞬间捕捉",
                "模糊的笔触和印象",
                "自然色彩的和谐运用",
                "水面倒影的波光粼粼",
                "季节变化的色彩表达"
            ],
            "color_philosophy": "捕捉自然光线的色彩变化，使用色彩分色技法，和谐的自然色调",
            "compositional_principles": [
                "光影引导视觉焦点",
                "模糊效果营造氛围",
                "色彩的和谐统一",
                "自然元素的有机布局"
            ],
            "mood": "宁静、优雅、自然、浪漫",
            "suitability": ["生活方式", "健康应用", "教育平台", "阅读应用"],
            "primary_colors": ["#7CB342", "#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B"],
            "typography": "优雅衬线字体，轻盈设计",
            "interaction": "淡入淡出，光效闪烁"
        },
        "kandinsky": {
            "name": "Wassily Kandinsky",
            "description": "抽象艺术先驱，以色彩音乐理论和几何抽象著称",
            "key_characteristics": [
                "色彩的旋律和节奏",
                "几何形状的交响",
                "点、线、面的和谐构成",
                "强烈的情感色彩表达",
                "抽象音乐般的构图"
            ],
            "color_philosophy": "色彩如音乐般具有节奏和旋律，几何形状代表不同的情感音符",
            "compositional_principles": [
                "几何形状的动态平衡",
                "色彩的节奏和对比",
                "线条的引导和流动",
                "抽象符号的情感表达"
            ],
            "mood": "动感、抽象、和谐、节奏感",
            "suitability": ["音乐应用", "艺术创作", "数据可视化", "创意平台"],
            "primary_colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
            "typography": "几何无衬线字体，动感设计",
            "interaction": "几何形状的律动动画"
        },
        "klee": {
            "name": "Paul Klee",
            "description": "几何抽象大师，以童趣和几何构成著称",
            "key_characteristics": [
                "童趣般的几何构成",
                "简单的线条和色块",
                "音乐性的视觉节奏",
                "微妙的色彩和谐",
                " playful的简约美学"
            ],
            "color_philosophy": "使用原色的微妙变化，简洁的色彩组合，童真的色彩表达",
            "compositional_principles": [
                "简单几何的巧妙组合",
                "线条的节奏感",
                "负空间的重要性",
                "童趣与专业的平衡"
            ],
            "mood": "童趣、简约、天真、温馨",
            "suitability": ["儿童应用", "教育平台", "创意游戏", "休闲应用"],
            "primary_colors": ["#FFB6C1", "#87CEEB", "#98FB98", "#F0E68C", "#DDA0DD"],
            "typography": "圆润字体，友好设计",
            "interaction": "弹跳动画，几何形状旋转"
        },
        "matisse": {
            "name": "Henri Matisse",
            "description": "野兽派大师，以大胆色块和剪纸风格著称",
            "key_characteristics": [
                "大胆的色块剪贴",
                "剪纸般的简洁造型",
                "强烈的色彩对比",
                "有机的流动曲线",
                "简约而有力量的表达"
            ],
            "color_philosophy": "使用大胆的纯色，剪纸般的造型，强烈的视觉冲击力",
            "compositional_principles": [
                "大色块的有机组合",
                "剪纸造型的简洁有力",
                "色彩的直接对比",
                "有机曲线的流畅表达"
            ],
            "mood": "活力、大胆、现代、自由",
            "suitability": ["时尚应用", "品牌展示", "创意平台", "艺术应用"],
            "primary_colors": ["#FF6B35", "#F7931E", "#FFD23F", "#06D6A0", "#118AB2"],
            "typography": "大胆无衬线字体，剪纸风格",
            "interaction": "色块滑动，剪纸展开动画"
        },
        "warhol": {
            "name": "Andy Warhol",
            "description": "波普艺术大师，以重复图像和鲜艳色彩著称",
            "key_characteristics": [
                "重复的图像排列",
                "鲜艳的波普色彩",
                "商业化的视觉语言",
                "丝网印刷效果",
                "流行文化的视觉表达"
            ],
            "color_philosophy": "使用鲜艳的高对比色彩，重复的图案，商业化的视觉冲击",
            "compositional_principles": [
                "重复图案创造视觉节奏",
                "高对比色吸引注意",
                "网格化的系统布局",
                "商业化的视觉语言"
            ],
            "mood": "前卫、流行、多彩、商业化",
            "suitability": ["电商应用", "社交媒体", "内容平台", "潮流应用"],
            "primary_colors": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF0000", "#00FF00"],
            "typography": "粗体无衬线字体，海报风格",
            "interaction": "闪烁效果，色彩循环切换"
        },
        "escher": {
            "name": "M.C. Escher",
            "description": "视错觉大师，以无限循环和不可能图形著称",
            "key_characteristics": [
                "无限循环的视觉错觉",
                "不可能的几何图形",
                "正负形巧妙转换",
                "数学与艺术的结合",
                "空间的矛盾与重构"
            ],
            "color_philosophy": "使用黑白灰的精确对比，简洁的色彩突出几何结构",
            "compositional_principles": [
                "正负形的巧妙转换",
                "无限循环的视觉效果",
                "几何结构的精确性",
                "空间矛盾的巧妙设计"
            ],
            "mood": "智慧、神秘、精确、无限",
            "suitability": ["游戏应用", "创意工具", "数据可视化", "教育平台"],
            "primary_colors": ["#2C3E50", "#34495E", "#7F8C8D", "#BDC3C7", "#ECF0F1"],
            "typography": "等宽字体，精确设计",
            "interaction": "翻转动画，循环滚动"
        },
        "hiroshige": {
            "name": "Utagawa Hiroshige",
            "description": "浮世绘大师，以日式风景和精美色彩著称",
            "key_characteristics": [
                "浮世绘的经典线条",
                "精致的自然描绘",
                "和风的传统美学",
                "季节的细腻表达",
                "留白的意境营造"
            ],
            "color_philosophy": "使用传统的和风色彩，精细的线条勾勒，留白的意境美学",
            "compositional_principles": [
                "传统和风的构图美学",
                "留白营造意境",
                "自然的细腻描绘",
                "线条的精确控制"
            ],
            "mood": "优雅、宁静、传统、精致",
            "suitability": ["文化应用", "旅游应用", "生活美学", "艺术展示"],
            "primary_colors": ["#E74C3C", "#F39C12", "#9B59B6", "#3498DB", "#1ABC9C"],
            "typography": "日式风格字体，优雅设计",
            "interaction": "淡入效果，流动的烟雾动画"
        },
        "klee_child": {
            "name": "Paul Klee - Child Style",
            "description": "克利的童趣风格，几何抽象与天真童趣的完美结合",
            "key_characteristics": [
                "儿童画般的简单线条",
                "几何形状的巧妙组合",
                "温暖柔和的色彩",
                "微妙的幽默感",
                "专业与童真的平衡"
            ],
            "color_philosophy": "使用温暖柔和的色调，简单的几何形状，营造童趣而专业的氛围",
            "compositional_principles": [
                "简单几何的有机组合",
                "童趣线条的专业处理",
                "温暖的色彩氛围",
                "微妙的幽默表达"
            ],
            "mood": "温馨、童趣、友好、舒适",
            "suitability": ["儿童应用", "家庭教育", "创意游戏", "休闲应用"],
            "primary_colors": ["#FFB6C1", "#87CEEB", "#98FB98", "#FFE4B5", "#DDA0DD"],
            "typography": "圆润友好字体，手写风格",
            "interaction": "弹跳动画，旋转效果"
        }
    }

    def __init__(self):
        self.demo_mode = True

    def generate_aesthetic_design(
        self,
        art_style: str,
        page_description: str,
        target_components: List[str],
        color_preference: Optional[str] = None,
        mood: Optional[str] = None,
        complexity: str = "medium",
        include_interactions: bool = True,
        include_assets: bool = True
    ) -> Dict[str, Any]:
        """
        生成完整的美学设计方案

        Args:
            art_style: 艺术风格
            page_description: 页面描述
            target_components: 目标组件列表
            color_preference: 颜色偏好
            mood: 情感基调
            complexity: 复杂度
            include_interactions: 是否包含交互
            include_assets: 是否包含素材
        """
        try:
            logger.info(f"Generating aesthetic design | Style: {art_style} | Components: {len(target_components)}")

            # 获取艺术风格信息
            style_info = self.ART_STYLES.get(art_style, self.ART_STYLES["van_gogh"])

            # 1. 生成美学分析
            aesthetic_analysis = self._generate_aesthetic_analysis(
                style_info, mood
            )

            # 2. 生成全局色彩方案
            global_color_palette = self._generate_color_palette(
                style_info, color_preference, complexity
            )

            # 3. 生成全局排版方案
            global_typography = self._generate_typography(style_info)

            # 4. 为每个组件生成设计方案
            component_designs = []
            visual_assets = []

            for component in target_components:
                design = self._generate_component_design(
                    component,
                    style_info,
                    global_color_palette,
                    global_typography,
                    page_description,
                    complexity
                )
                component_designs.append(design)

                # 生成视觉素材提示词
                if include_assets:
                    assets = self._generate_visual_assets(
                        component,
                        style_info,
                        global_color_palette
                    )
                    visual_assets.extend(assets)

            # 5. 生成交互设计
            interactions = []
            if include_interactions:
                interactions = self._generate_interactions(
                    target_components,
                    style_info,
                    complexity
                )

            # 6. 生成设计摘要
            design_summary = self._generate_design_summary(
                style_info,
                aesthetic_analysis,
                global_color_palette,
                component_designs,
                page_description
            )

            logger.info(f"✅ Aesthetic design generated | {len(component_designs)} components | {len(visual_assets)} assets")

            return {
                "aesthetic_analysis": aesthetic_analysis,
                "global_color_palette": global_color_palette,
                "global_typography": global_typography,
                "component_designs": component_designs,
                "interactions": interactions,
                "visual_assets": visual_assets,
                "design_summary": design_summary
            }

        except Exception as e:
            logger.error(f"Failed to generate aesthetic design: {e}")
            raise

    def _generate_aesthetic_analysis(
        self,
        style_info: Dict[str, Any],
        mood: Optional[str]
    ) -> Dict[str, Any]:
        """生成美学分析"""
        return {
            "style_name": style_info["name"],
            "style_description": style_info["description"],
            "key_characteristics": style_info["key_characteristics"],
            "color_philosophy": style_info["color_philosophy"],
            "compositional_principles": style_info["compositional_principles"],
            "mood": mood or style_info["mood"],
            "suitability": style_info["suitability"]
        }

    def _generate_color_palette(
        self,
        style_info: Dict[str, Any],
        color_preference: Optional[str],
        complexity: str
    ) -> Dict[str, Any]:
        """生成色彩方案"""
        primary_colors = style_info["primary_colors"]

        # 如果有用户偏好，调整颜色
        if color_preference:
            primary_colors = self._adjust_color_preference(primary_colors, color_preference)

        # 根据复杂度调整颜色数量
        num_gradient_colors = 2 if complexity == "low" else (4 if complexity == "medium" else 6)
        gradient_colors = primary_colors[:num_gradient_colors]

        return {
            "primary": primary_colors[0],
            "secondary": primary_colors[1] if len(primary_colors) > 1 else primary_colors[0],
            "accent": primary_colors[2] if len(primary_colors) > 2 else primary_colors[0],
            "background": "#FFFFFF" if complexity == "low" else "#F8F9FA",
            "surface": "#FFFFFF" if complexity == "low" else "#FFFFFF",
            "text": "#1A1A1A",
            "gradient_colors": gradient_colors
        }

    def _adjust_color_preference(self, colors: List[str], preference: str) -> List[str]:
        """根据用户偏好调整颜色"""
        # 简化的颜色调整逻辑
        preference_map = {
            "warm": ["#FF6B35", "#F7931E", "#FFD23F", "#FF6B6B", "#E74C3C"],
            "cool": ["#4ECDC4", "#45B7D1", "#3498DB", "#1ABC9C", "#118AB2"],
            "dark": ["#2C3E50", "#34495E", "#1A1A1A", "#0D1B2A", "#1B4965"],
            "light": ["#F8F9FA", "#FFFFFF", "#E9ECEF", "#DEE2E6", "#CED4DA"]
        }
        return preference_map.get(preference.lower(), colors)

    def _generate_typography(self, style_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成排版方案"""
        return {
            "heading_font": "Inter" if "无衬线" in style_info["typography"] else "Merriweather",
            "body_font": "Inter",
            "heading_weights": {
                "h1": 700,
                "h2": 600,
                "h3": 600,
                "h4": 500,
                "h5": 500,
                "h6": 400
            },
            "line_heights": {
                "heading": 1.2,
                "body": 1.6,
                "tight": 1.3
            },
            "letter_spacing": {
                "heading": "-0.02em",
                "body": "0",
                "wide": "0.05em"
            }
        }

    def _generate_component_design(
        self,
        component: str,
        style_info: Dict[str, Any],
        color_palette: Dict[str, Any],
        typography: Dict[str, Any],
        page_description: str,
        complexity: str
    ) -> Dict[str, Any]:
        """生成组件设计方案"""

        # 根据组件类型生成特定设计
        component_config = self._get_component_config(component, style_info, color_palette)

        # 生成CSS代码
        css_code = self._generate_component_css(component, component_config)

        # 生成Tailwind类名
        tailwind_classes = self._generate_tailwind_classes(component, component_config)

        return {
            "component": component,
            "layout_description": component_config["layout_description"],
            "colors": {
                "primary": color_palette["primary"],
                "secondary": color_palette["secondary"],
                "accent": color_palette["accent"],
                "background": color_palette["background"],
                "surface": color_palette["surface"],
                "text": color_palette["text"]
            },
            "style": {
                "component_type": component,
                "border_radius": component_config["border_radius"],
                "shadows": component_config["shadows"],
                "padding": component_config["padding"],
                "margin": component_config["margin"]
            },
            "typography": typography,
            "interaction": None,
            "visual_assets": [],
            "css_code": css_code,
            "tailwind_classes": tailwind_classes
        }

    def _get_component_config(
        self,
        component: str,
        style_info: Dict[str, Any],
        color_palette: Dict[str, Any]
    ) -> Dict[str, Any]:
        """获取组件配置"""
        configs = {
            "hero_banner": {
                "layout_description": "大尺寸主横幅，使用艺术风格的渐变背景和动态视觉元素",
                "border_radius": "0px",
                "shadows": ["none"],
                "padding": "80px 40px",
                "margin": "0"
            },
            "header": {
                "layout_description": "顶部导航栏，简洁优雅，与整体艺术风格协调",
                "border_radius": "0px",
                "shadows": ["0 2px 8px rgba(0,0,0,0.1)"],
                "padding": "16px 32px",
                "margin": "0"
            },
            "sidebar": {
                "layout_description": "侧边导航，使用艺术风格的图标和交互效果",
                "border_radius": "0px",
                "shadows": ["2px 0 8px rgba(0,0,0,0.1)"],
                "padding": "24px 20px",
                "margin": "0"
            },
            "card": {
                "layout_description": "卡片组件，艺术风格的圆角和阴影效果",
                "border_radius": "16px",
                "shadows": ["0 4px 16px rgba(0,0,0,0.1)", "0 8px 32px rgba(0,0,0,0.08)"],
                "padding": "24px",
                "margin": "16px"
            },
            "button": {
                "layout_description": "按钮组件，结合艺术风格的色彩和交互动效",
                "border_radius": "12px",
                "shadows": ["0 4px 12px rgba(0,0,0,0.15)"],
                "padding": "12px 24px",
                "margin": "8px"
            },
            "background": {
                "layout_description": "页面背景，艺术风格的渐变或纹理",
                "border_radius": "0px",
                "shadows": ["none"],
                "padding": "0",
                "margin": "0"
            },
            "modal": {
                "layout_description": "模态框，艺术风格的弹窗设计",
                "border_radius": "20px",
                "shadows": ["0 16px 48px rgba(0,0,0,0.3)"],
                "padding": "32px",
                "margin": "0"
            },
            "form_input": {
                "layout_description": "表单输入，艺术风格的边框和焦点效果",
                "border_radius": "10px",
                "shadows": ["none", "0 0 0 3px rgba(0,0,0,0.1)"],
                "padding": "12px 16px",
                "margin": "8px 0"
            }
        }

        return configs.get(component, configs["card"])

    def _generate_component_css(self, component: str, config: Dict[str, Any]) -> str:
        """生成组件CSS代码"""
        css = f"""
/* {component.upper()} - {config['layout_description']} */
.{component} {{
    border-radius: {config['border_radius']};
    padding: {config['padding']};
    margin: {config['margin']};
}}

.{component}:hover {{
    box-shadow: {', '.join(config['shadows']) if config['shadows'] else 'none'};
    transform: translateY(-2px);
    transition: all 0.3s ease;
}}
"""
        return css.strip()

    def _generate_tailwind_classes(self, component: str, config: Dict[str, Any]) -> str:
        """生成Tailwind CSS类名"""
        classes_map = {
            "hero_banner": "w-full min-h-screen flex items-center justify-center p-20 rounded-none",
            "header": "w-full px-8 py-4 rounded-none shadow-sm",
            "sidebar": "h-screen w-64 p-6 shadow-md rounded-none",
            "card": "rounded-2xl p-6 m-4 shadow-lg hover:shadow-xl transition-all duration-300",
            "button": "px-6 py-3 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5",
            "background": "w-full h-full rounded-none",
            "modal": "rounded-[20px] p-8 shadow-2xl",
            "form_input": "px-4 py-3 rounded-lg focus:outline-none focus:ring-2"
        }

        return classes_map.get(component, classes_map["card"])

    def _generate_visual_assets(
        self,
        component: str,
        style_info: Dict[str, Any],
        color_palette: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """生成视觉素材提示词"""
        assets = []

        # 根据组件类型生成相应的素材提示词
        asset_prompts = self._get_asset_prompts(component, style_info, color_palette)

        for asset_type, prompt in asset_prompts.items():
            assets.append({
                "asset_type": asset_type,
                "component": component,
                "description": f"{asset_type} for {component}",
                "prompt": prompt,
                "size": "512x512",
                "style_notes": f"Based on {style_info['name']} style"
            })

        return assets

    def _get_asset_prompts(
        self,
        component: str,
        style_info: Dict[str, Any],
        color_palette: Dict[str, Any]
    ) -> Dict[str, str]:
        """获取素材提示词"""

        style_desc = style_info["description"]
        color_desc = f"with colors {', '.join(style_info['primary_colors'][:3])}"

        prompts = {
            "hero_banner": {
                "image": f"A stunning hero banner background in {style_info['name']} style, {style_desc}, {color_desc}, high quality, professional design"
            },
            "header": {
                "icon": f"A minimalist logo icon in {style_info['name']} style, {color_desc}, clean design"
            },
            "card": {
                "icon": f"An elegant card icon in {style_info['name']} style, {color_desc}, professional"
            },
            "button": {
                "icon": f"A modern button icon in {style_info['name']} style, {color_desc}, simple design"
            },
            "background": {
                "pattern": f"A subtle background pattern in {style_info['name']} style, {color_desc}, minimal and elegant"
            },
            "modal": {
                "illustration": f"A beautiful modal illustration in {style_info['name']} style, {style_desc}, {color_desc}"
            }
        }

        return prompts.get(component, {})

    def _generate_interactions(
        self,
        components: List[str],
        style_info: Dict[str, Any],
        complexity: str
    ) -> List[Dict[str, Any]]:
        """生成交互设计"""
        interactions = []

        for component in components:
            interaction = {
                "interaction_type": "hover",
                "component": component,
                "effect": f"Elegant {style_info['interaction']}",
                "duration": "300ms",
                "easing": "ease-in-out",
                "description": f"Hover effect inspired by {style_info['name']}'s style"
            }
            interactions.append(interaction)

        return interactions

    def _generate_design_summary(
        self,
        style_info: Dict[str, Any],
        aesthetic_analysis: Dict[str, Any],
        color_palette: Dict[str, Any],
        component_designs: List[Dict[str, Any]],
        page_description: str
    ) -> str:
        """生成设计摘要"""

        summary = f"""
# {style_info['name']} Style Aesthetic Design

## Overview
This design is inspired by {style_info['name']}'s artistic style, combining {style_info['description']}

## Color Palette
- Primary: {color_palette['primary']}
- Secondary: {color_palette['secondary']}
- Accent: {color_palette['accent']}
- Background: {color_palette['background']}

## Key Characteristics
{chr(10).join([f"- {char}" for char in aesthetic_analysis['key_characteristics']])}

## Components Designed
{chr(10).join([f"- {design['component'].upper()}: {design['layout_description']}" for design in component_designs])}

## Mood & Atmosphere
The design creates a {aesthetic_analysis['mood']} atmosphere, perfectly suited for {', '.join(aesthetic_analysis['suitability'])}.

## Application
This aesthetic design is optimized for: {page_description}
        """.strip()

        return summary


# 全局服务实例
aesthetic_service = AestheticGenerationService()
