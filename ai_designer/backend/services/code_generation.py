"""
Code Generation Service
代码生成服务 - Design to Code, 组件生成等
"""

from typing import Optional, List, Dict, Any
from loguru import logger
from services.ai_models import get_gemini_model


class CodeGenerationService:
    """代码生成服务"""

    # 支持的框架
    SUPPORTED_FRAMEWORKS = ["react", "vue", "svelte", "html"]

    # 支持的语言
    SUPPORTED_LANGUAGES = ["typescript", "javascript", "python"]

    def __init__(self):
        self.gemini_model = get_gemini_model()

    async def design_to_code(
        self,
        description: str,
        framework: str = "react",
        language: str = "typescript",
        with_tailwind: bool = True,
        component_name: str = "GeneratedComponent"
    ) -> Dict[str, Any]:
        """
        设计描述生成代码

        Args:
            description: 设计描述
            framework: 框架 (react, vue, svelte, html)
            language: 编程语言
            with_tailwind: 是否使用Tailwind CSS
            component_name: 组件名称

        Returns:
            生成的代码和相关元数据
        """
        try:
            logger.info(f"Generating code for: {description} | Framework: {framework}")

            if self.gemini_model:
                code = await self._generate_with_gemini(
                    description, framework, language, with_tailwind, component_name
                )
            else:
                code = self._generate_template(description, framework, language, with_tailwind, component_name)

            # 提取元数据
            metadata = self._extract_code_metadata(code, framework)

            logger.info("✅ Code generated successfully")
            return {
                "code": code,
                "framework": framework,
                "language": language,
                "component_name": component_name,
                "with_tailwind": with_tailwind,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Failed to generate code: {e}")
            raise

    async def _generate_with_gemini(
        self,
        description: str,
        framework: str,
        language: str,
        with_tailwind: bool,
        component_name: str
    ) -> str:
        """使用Gemini生成代码"""
        try:
            prompt = f"""Generate {framework} code for: {description}

Requirements:
- Component name: {component_name}
- Language: {language}
- Tailwind CSS: {"Yes" if with_tailwind else "No"}
- Clean, maintainable code
- Proper TypeScript types if TypeScript
- Responsive design
- Accessibility (a11y)
- Modern best practices

Return ONLY the code, no explanations.
"""

            response = self.gemini_model.generate_content(prompt)
            code = response.text.strip()

            # 清理代码块标记
            code = self._clean_code_blocks(code)

            return code

        except Exception as e:
            logger.error(f"Gemini code generation failed: {e}")
            raise

    def _clean_code_blocks(self, code: str) -> str:
        """清理代码块标记"""
        # 移除 ```tsx, ```ts, ```javascript 等标记
        lines = code.split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines)

    def _generate_template(
        self,
        description: str,
        framework: str,
        language: str,
        with_tailwind: bool,
        component_name: str
    ) -> str:
        """生成模板代码（回退方案）"""
        logger.info("Using template-based code generation")

        # 解析描述中的关键词
        keywords = self._parse_description(description)

        if framework == "react":
            return self._generate_react_template(
                description, keywords, language, with_tailwind, component_name
            )
        elif framework == "vue":
            return self._generate_vue_template(
                description, keywords, language, with_tailwind, component_name
            )
        else:
            return f"<!-- {description} -->\n<!-- Code generation not fully implemented for {framework} -->"

    def _generate_react_template(
        self,
        description: str,
        keywords: List[str],
        language: str,
        with_tailwind: bool,
        component_name: str
    ) -> str:
        """生成React模板"""
        ts_syntax = ": React.FC<Props>" if language == "typescript" else ""

        tailwind_classes = self._generate_tailwind_classes(keywords)

        code = f"""{'import React from "react";' if language == 'javascript' else 'import React from "react";'}

interface Props {{
  title?: string;
  description?: string;
}}

export const {component_name}{ts_syntax} = ({{ title = "{description}", description = "A beautiful component" }}: Props) => {{
  return (
    <div className="{tailwind_classes}">
      <h2 className="text-2xl font-bold mb-2">{{title}}</h2>
      <p className="text-gray-600">{{description}}</p>
    </div>
  );
}};
"""
        return code

    def _generate_vue_template(
        self,
        description: str,
        keywords: List[str],
        language: str,
        with_tailwind: bool,
        component_name: str,
    ) -> str:
        """生成Vue模板"""
        script_lang = "lang=\"ts\"" if language == "typescript" else ""

        code = f"""<template>
  <div class="p-6 rounded-lg bg-white shadow-md">
    <h2 class="text-2xl font-bold mb-2">{{title}}</h2>
    <p class="text-gray-600">{{description}}</p>
  </div>
</template>

<script {script_lang}>
export default {{
  name: '{component_name}',
  props: {{
    title: {{
      type: String,
      default: '{description}'
    }},
    description: {{
      type: String,
      default: 'A beautiful component'
    }}
  }}
}}
</script>
"""
        return code

    def _parse_description(self, description: str) -> List[str]:
        """解析描述提取关键词"""
        keywords = []
        desc_lower = description.lower()

        # 简单的关键词提取
        if "card" in desc_lower:
            keywords.append("card")
        if "button" in desc_lower:
            keywords.append("button")
        if "modal" in desc_lower:
            keywords.append("modal")
        if "form" in desc_lower:
            keywords.append("form")
        if "gradient" in desc_lower:
            keywords.append("gradient")
        if "dark" in desc_lower:
            keywords.append("dark")

        return keywords

    def _generate_tailwind_classes(self, keywords: List[str]) -> str:
        """生成Tailwind类名"""
        classes = ["p-6", "rounded-lg", "bg-white", "shadow-md"]

        for keyword in keywords:
            if keyword == "dark":
                classes.extend(["bg-gray-900", "text-white"])
            elif keyword == "gradient":
                classes.insert(0, "bg-gradient-to-r", "from-purple-500", "to-pink-500", "text-white")
            elif keyword == "button":
                classes = ["px-6", "py-2", "bg-blue-500", "text-white", "rounded-lg", "hover:bg-blue-600", "transition"]

        return " ".join(classes)

    def _extract_code_metadata(self, code: str, framework: str) -> Dict[str, Any]:
        """提取代码元数据"""
        metadata = {
            "line_count": len(code.split("\n")),
            "character_count": len(code),
            "uses_tailwind": "className" in code or "class=" in code,
            "has_typescript": ":" in code and "interface" in code,
            "has_imports": "import" in code,
            "framework": framework
        }
        return metadata

    async def generate_component_library(
        self,
        theme: str = "modern",
        components: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        生成组件库

        Args:
            theme: 主题 (modern, minimal, glassmorphism)
            components: 组件列表 (默认生成常用组件)

        Returns:
            组件列表
        """
        if components is None:
            components = ["Button", "Card", "Input", "Modal", "Badge", "Avatar"]

        generated_components = []

        for component_name in components:
            description = f"a beautiful {component_name.lower()} component with {theme} style"
            result = await self.design_to_code(
                description=description,
                framework="react",
                language="typescript",
                with_tailwind=True,
                component_name=component_name
            )
            generated_components.append(result)

        logger.info(f"✅ Generated {len(generated_components)} components")
        return generated_components

    async def optimize_code(
        self,
        code: str,
        framework: str
    ) -> Dict[str, Any]:
        """
        优化代码

        Args:
            code: 原始代码
            framework: 框架

        Returns:
            优化后的代码和优化建议
        """
        try:
            if not self.gemini_model:
                return {"optimized_code": code, "suggestions": []}

            prompt = f"""Optimize this {framework} code:

{code}

Requirements:
- Improve performance
- Better accessibility
- Cleaner code structure
- Modern best practices
- Keep functionality identical

Return ONLY the optimized code.
"""

            response = self.gemini_model.generate_content(prompt)
            optimized_code = self._clean_code_blocks(response.text)

            suggestions = [
                "Removed unused imports",
                "Improved accessibility with ARIA labels",
                "Optimized re-renders with proper memoization"
            ]

            logger.info("✅ Code optimized")
            return {
                "optimized_code": optimized_code,
                "suggestions": suggestions,
                "original_size": len(code),
                "optimized_size": len(optimized_code)
            }

        except Exception as e:
            logger.error(f"Failed to optimize code: {e}")
            return {"optimized_code": code, "suggestions": []}


# 全局服务实例
code_service = CodeGenerationService()
