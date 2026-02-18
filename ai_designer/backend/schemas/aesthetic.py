"""
Aesthetic Design Schemas
美学设计生成 - 艺术风格参考与完整前端美学方案
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum


class ArtMasterStyle(str, Enum):
    """艺术巨匠风格"""
    VAN_GOGH = "van_gogh"  # 梵高 - 星空风格，旋涡笔触
    PICASSO = "picasso"  # 毕加索 - 立体主义，几何碎片
    DALI = "dali"  # 达利 - 超现实主义，梦境
    MONET = "monet"  # 莫奈 - 印象派，光影色彩
    KANDINSKY = "kandinsky"  # 康定斯基 - 抽象表现主义
    KLEE = "klee"  # 克利 - 几何抽象，童趣
    MATISSE = "matisse"  # 马蒂斯 - 剪纸风格，大胆色块
    WARHOL = "warhol"  # 沃霍尔 - 波普艺术，重复图像
    KANDINSKY_ABSTRACT = "kandinsky_abstract"  # 康定斯基抽象
    ESCHER = "escher"  # 埃舍尔 - 视错觉，无限循环
    HIROSHIGE = "hiroshige"  # 浮世绘，日式风格
    KLEE_CHILD = "klee_child"  # 克利童趣风格


class UIComponent(str, Enum):
    """UI组件类型"""
    HERO_BANNER = "hero_banner"  # 主横幅
    HEADER = "header"  # 顶部导航
    SIDEBAR = "sidebar"  # 侧边栏
    CARD = "card"  # 卡片
    BUTTON = "button"  # 按钮
    BACKGROUND = "background"  # 背景纹理
    MODAL = "modal"  # 模态框
    TOOLTIP = "tooltip"  # 提示框
    FORM_INPUT = "form_input"  # 表单输入
    ICON = "icon"  # 图标
    BADGE = "badge"  # 徽章
    PROGRESS = "progress"  # 进度条
    TAB = "tab"  # 标签页
    TABLE = "table"  # 表格


class InteractionType(str, Enum):
    """交互类型"""
    HOVER = "hover"  # 悬停
    CLICK = "click"  # 点击
    TRANSITION = "transition"  # 过渡
    ANIMATION = "animation"  # 动画
    SCROLL = "scroll"  # 滚动


class ColorPalette(BaseModel):
    """色彩方案"""
    primary: str = Field(..., description="主色调")
    secondary: str = Field(..., description="次要色调")
    accent: str = Field(..., description="强调色")
    background: str = Field(..., description="背景色")
    surface: str = Field(..., description="表面色")
    text: str = Field(..., description="文本色")
    gradient_colors: List[str] = Field(default_factory=list, description="渐变色列表")


class Typography(BaseModel):
    """排版方案"""
    heading_font: str = Field(..., description="标题字体")
    body_font: str = Field(..., description="正文字体")
    heading_weights: Dict[str, int] = Field(default_factory=dict, description="标题字重")
    line_heights: Dict[str, float] = Field(default_factory=dict, description="行高")
    letter_spacing: Dict[str, str] = Field(default_factory=dict, description="字间距")


class ComponentStyle(BaseModel):
    """组件样式"""
    component_type: UIComponent = Field(..., description="组件类型")
    colors: Dict[str, str] = Field(default_factory=dict, description="颜色")
    border_radius: str = Field(default="8px", description="圆角")
    shadows: List[str] = Field(default_factory=list, description="阴影")
    padding: str = Field(default="16px", description="内边距")
    margin: str = Field(default="0", description="外边距")


class InteractionDesign(BaseModel):
    """交互动效设计"""
    interaction_type: InteractionType = Field(..., description="交互类型")
    component: str = Field(..., description="组件")
    effect: str = Field(..., description="效果描述")
    duration: str = Field(default="300ms", description="持续时间")
    easing: str = Field(default="ease-in-out", description="缓动函数")
    description: str = Field(..., description="详细描述")


class VisualAsset(BaseModel):
    """视觉素材"""
    asset_type: str = Field(..., description="素材类型 (image, svg, icon, pattern)")
    component: UIComponent = Field(..., description="所属组件")
    description: str = Field(..., description="描述")
    prompt: str = Field(..., description="AI生成提示词")
    size: str = Field(default="512x512", description="尺寸")
    style_notes: str = Field(default="", description="风格备注")


class ComponentDesign(BaseModel):
    """组件设计方案"""
    component: UIComponent = Field(..., description="组件类型")
    layout_description: str = Field(..., description="布局描述")
    colors: ColorPalette = Field(..., description="色彩方案")
    style: ComponentStyle = Field(..., description="样式配置")
    typography: Optional[Typography] = Field(None, description="排版")
    interaction: Optional[InteractionDesign] = Field(None, description="交互")
    visual_assets: List[VisualAsset] = Field(default_factory=list, description="视觉素材")
    css_code: str = Field(..., description="CSS代码片段")
    tailwind_classes: str = Field(..., description="Tailwind CSS类名")


class AestheticAnalysis(BaseModel):
    """美学分析"""
    style_name: str = Field(..., description="风格名称")
    style_description: str = Field(..., description="风格描述")
    key_characteristics: List[str] = Field(default_factory=list, description="关键特征")
    color_philosophy: str = Field(..., description="色彩哲学")
    compositional_principles: List[str] = Field(default_factory=list, description="构图原则")
    mood: str = Field(..., description="情感基调")
    suitability: List[str] = Field(default_factory=list, description="适用场景")


class AestheticDesignRequest(BaseModel):
    """美学设计生成请求"""
    art_style: ArtMasterStyle = Field(
        ...,
        description="参考的艺术巨匠风格"
    )
    page_description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="页面描述（布局、功能、场景）"
    )
    target_components: List[UIComponent] = Field(
        ...,
        description="需要设计的组件列表"
    )
    color_preference: Optional[str] = Field(
        None,
        description="用户颜色偏好"
    )
    mood: Optional[str] = Field(
        None,
        description="期望的情感基调"
    )
    complexity: str = Field(
        "medium",
        description="复杂度 (low, medium, high)"
    )
    include_interactions: bool = Field(
        True,
        description="是否包含交互设计"
    )
    include_assets: bool = Field(
        True,
        description="是否生成视觉素材提示词"
    )

    @field_validator('page_description')
    @classmethod
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Page description cannot be empty')
        return v.strip()


class AestheticDesignResponse(BaseModel):
    """美学设计生成响应"""
    success: bool = Field(..., description="是否成功")
    request_id: str = Field(..., description="请求ID")
    generation_time: float = Field(..., description="生成时间(秒)")

    # 艺术风格分析
    aesthetic_analysis: AestheticAnalysis = Field(..., description="美学分析")

    # 全局色彩和排版
    global_color_palette: ColorPalette = Field(..., description="全局色彩方案")
    global_typography: Typography = Field(..., description="全局排版")

    # 组件设计
    component_designs: List[ComponentDesign] = Field(..., description="组件设计方案")

    # 交互动效
    interactions: List[InteractionDesign] = Field(default_factory=list, description="交互动效设计")

    # 视觉素材提示词
    visual_assets: List[VisualAsset] = Field(default_factory=list, description="视觉素材提示词")

    # 完整设计方案摘要
    design_summary: str = Field(..., description="设计摘要")


class ArtStylePresetsResponse(BaseModel):
    """艺术风格预设响应"""
    styles: List[Dict[str, Any]] = Field(..., description="可用风格列表")
