"""
Skills System - 领域特定扩展包管理系统

这个模块提供了管理技能（Skills）的基础架构，每个 Skill 是一个领域特定的扩展包，
提供专业知识、工作流程（SOPs）和可执行工具/脚本。

Skills 可以：
- 提供特定领域的专家知识
- 定义标准化的工作流程
- 集成可执行的工具或脚本
- 扩展助手的能力范围
"""

import os
import json
import importlib.util
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class SkillStatus(Enum):
    """技能状态枚举"""
    AVAILABLE = "available"    # 可用
    LOADED = "loaded"         # 已加载
    ERROR = "error"           # 加载错误


@dataclass
class SkillMetadata:
    """技能元数据"""
    name: str                           # 技能名称
    description: str                    # 技能描述
    version: str = "1.0.0"              # 版本号
    author: str = ""                    # 作者
    category: str = "general"          # 分类
    dependencies: List[str] = field(default_factory=list)  # 依赖的技能
    capabilities: List[str] = field(default_factory=list)   # 能力列表
    required_tools: List[str] = field(default_factory=list) # 需要的工具
    base_directory: Optional[str] = None  # 基础目录路径


class Skill:
    """技能基类
    
    所有自定义技能都应继承此类并实现相应方法。
    """
    
    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata
        self.status = SkillStatus.AVAILABLE
        self._loaded = False
    
    def load(self) -> bool:
        """加载技能
        
        Returns:
            bool: 是否加载成功
        """
        try:
            # 检查依赖
            for dep in self.metadata.dependencies:
                if not self._check_dependency(dep):
                    print(f"警告: 依赖项 {dep} 未满足")
                    return False
            
            # 执行自定义加载逻辑
            self._on_load()
            self.status = SkillStatus.LOADED
            self._loaded = True
            return True
        except Exception as e:
            self.status = SkillStatus.ERROR
            print(f"加载技能失败: {e}")
            return False
    
    def unload(self) -> None:
        """卸载技能"""
        try:
            self._on_unload()
            self.status = SkillStatus.AVAILABLE
            self._loaded = False
        except Exception as e:
            print(f"卸载技能时出错: {e}")
    
    def _check_dependency(self, dependency: str) -> bool:
        """检查依赖是否满足
        
        子类可以重写此方法以实现自定义依赖检查
        """
        return True
    
    def _on_load(self) -> None:
        """加载时的回调函数
        
        子类应重写此方法以实现自定义加载逻辑
        """
        pass
    
    def _on_unload(self) -> None:
        """卸载时的回调函数
        
        子类应重写此方法以实现自定义卸载逻辑
        """
        pass
    
    def execute(self, action: str, **kwargs) -> Any:
        """执行技能动作
        
        Args:
            action: 动作名称
            **kwargs: 动作参数
            
        Returns:
            执行结果
        """
        if not self._loaded:
            raise RuntimeError(f"技能 {self.metadata.name} 未加载")
        
        action_method = getattr(self, f"_action_{action}", None)
        if action_method is None:
            raise ValueError(f"未知的动作: {action}")
        
        return action_method(**kwargs)
    
    def get_capabilities(self) -> List[str]:
        """获取技能能力列表"""
        return self.metadata.capabilities
    
    def is_loaded(self) -> bool:
        """检查技能是否已加载"""
        return self._loaded


class SkillManager:
    """技能管理器
    
    负责发现、加载和管理所有可用的技能。
    """
    
    def __init__(self, skills_directory: str = "skills"):
        self.skills_directory = Path(skills_directory)
        self._skills: Dict[str, Skill] = {}
        self._skill_configs: Dict[str, Dict] = {}
    
    def discover_skills(self) -> List[SkillMetadata]:
        """发现所有可用的技能
        
        Returns:
            技能元数据列表
        """
        metadata_list = []
        
        if not self.skills_directory.exists():
            return metadata_list
        
        for skill_dir in self.skills_directory.iterdir():
            if not skill_dir.is_dir():
                continue
            
            # 查找技能配置文件
            config_file = skill_dir / "skill_config.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        metadata = SkillMetadata(
                            name=config.get('name', skill_dir.name),
                            description=config.get('description', ''),
                            version=config.get('version', '1.0.0'),
                            author=config.get('author', ''),
                            category=config.get('category', 'general'),
                            dependencies=config.get('dependencies', []),
                            capabilities=config.get('capabilities', []),
                            required_tools=config.get('required_tools', []),
                            base_directory=str(skill_dir)
                        )
                        self._skill_configs[metadata.name] = config
                        metadata_list.append(metadata)
                except Exception as e:
                    print(f"加载技能配置失败 {skill_dir}: {e}")
        
        return metadata_list
    
    def load_skill(self, skill_name: str) -> bool:
        """加载指定技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            bool: 是否加载成功
        """
        if skill_name in self._skills and self._skills[skill_name].is_loaded():
            print(f"技能 {skill_name} 已经加载")
            return True
        
        # 获取技能配置
        config = self._skill_configs.get(skill_name)
        if not config:
            print(f"未找到技能: {skill_name}")
            return False
        
        try:
            # 加载技能模块
            skill_module_path = Path(config.get('base_directory', skill_name)) / f"{skill_name}.py"
            if not skill_module_path.exists():
                # 尝试从其他路径加载
                skill_dir = self.skills_directory / skill_name
                skill_module_path = skill_dir / f"{skill_name}.py"
            
            if not skill_module_path.exists():
                print(f"未找到技能模块: {skill_module_path}")
                return False
            
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(skill_name, skill_module_path)
            if spec is None or spec.loader is None:
                print(f"无法加载模块: {skill_module_path}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 查找技能类
            skill_class = getattr(module, skill_name.capitalize() + 'Skill', None)
            if skill_class is None:
                # 尝试其他可能的命名方式
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Skill) and attr != Skill:
                        skill_class = attr
                        break
            
            if skill_class is None:
                print(f"未找到技能类: {skill_name}")
                return False
            
            # 创建并加载技能实例
            metadata = SkillMetadata(
                name=config['name'],
                description=config['description'],
                version=config.get('version', '1.0.0'),
                author=config.get('author', ''),
                category=config.get('category', 'general'),
                dependencies=config.get('dependencies', []),
                capabilities=config.get('capabilities', []),
                required_tools=config.get('required_tools', []),
                base_directory=config.get('base_directory')
            )
            
            skill = skill_class(metadata)
            if skill.load():
                self._skills[skill_name] = skill
                print(f"成功加载技能: {skill_name}")
                return True
            else:
                print(f"加载技能失败: {skill_name}")
                return False
                
        except Exception as e:
            print(f"加载技能时发生错误: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def unload_skill(self, skill_name: str) -> bool:
        """卸载指定技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            bool: 是否卸载成功
        """
        if skill_name not in self._skills:
            print(f"技能 {skill_name} 未加载")
            return False
        
        try:
            self._skills[skill_name].unload()
            del self._skills[skill_name]
            print(f"成功卸载技能: {skill_name}")
            return True
        except Exception as e:
            print(f"卸载技能时发生错误: {e}")
            return False
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """获取已加载的技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            技能实例或 None
        """
        return self._skills.get(skill_name)
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """列出所有技能及其状态
        
        Returns:
            技能信息列表
        """
        skill_list = []
        
        # 已加载的技能
        for name, skill in self._skills.items():
            skill_list.append({
                'name': name,
                'status': skill.status.value,
                'loaded': skill.is_loaded(),
                'capabilities': skill.get_capabilities()
            })
        
        # 未加载但可用的技能
        for name, config in self._skill_configs.items():
            if name not in self._skills:
                skill_list.append({
                    'name': name,
                    'status': 'available',
                    'loaded': False,
                    'capabilities': config.get('capabilities', [])
                })
        
        return skill_list
    
    def execute_skill(self, skill_name: str, action: str, **kwargs) -> Any:
        """执行技能动作
        
        Args:
            skill_name: 技能名称
            action: 动作名称
            **kwargs: 动作参数
            
        Returns:
            执行结果
        """
        skill = self.get_skill(skill_name)
        if skill is None:
            raise ValueError(f"技能 {skill_name} 未加载")
        
        return skill.execute(action, **kwargs)


# 全局技能管理器实例
_global_skill_manager: Optional[SkillManager] = None


def get_skill_manager() -> SkillManager:
    """获取全局技能管理器实例"""
    global _global_skill_manager
    if _global_skill_manager is None:
        _global_skill_manager = SkillManager()
        _global_skill_manager.discover_skills()
    return _global_skill_manager


def create_skill(name: str, description: str, **kwargs) -> None:
    """创建新技能的模板
    
    Args:
        name: 技能名称
        description: 技能描述
        **kwargs: 其他配置项
    """
    skills_dir = Path("skills")
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建配置文件
    config = {
        "name": name,
        "description": description,
        "version": kwargs.get('version', '1.0.0'),
        "author": kwargs.get('author', ''),
        "category": kwargs.get('category', 'general'),
        "dependencies": kwargs.get('dependencies', []),
        "capabilities": kwargs.get('capabilities', []),
        "required_tools": kwargs.get('required_tools', []),
        "base_directory": str(skill_dir)
    }
    
    config_file = skill_dir / "skill_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 创建技能实现文件模板
    skill_class_name = name.capitalize() + 'Skill'
    skill_template = f'''"""
{description}
"""

from skills import Skill, SkillMetadata


class {skill_class_name}(Skill):
    """{description}"""
    
    def _on_load(self):
        """加载时的初始化"""
        print(f"加载 {{self.metadata.name}} 技能...")
        # 在这里添加你的初始化逻辑
        
    def _on_unload(self):
        """卸载时的清理"""
        print(f"卸载 {{self.metadata.name}} 技能...")
        # 在这里添加你的清理逻辑
    
    def _action_execute(self, **kwargs):
        """执行主动作
        
        这是一个示例动作，你可以添加更多动作方法
        """
        print(f"执行 {{self.metadata.name}} 的主动作")
        # 实现你的逻辑
        return {{"status": "success"}}
'''
    
    skill_file = skill_dir / f"{name}.py"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill_template)
    
    print(f"技能模板已创建: {skill_dir}")


if __name__ == "__main__":
    # 示例：使用技能管理器
    manager = SkillManager()
    
    # 发现技能
    print("发现技能...")
    skills = manager.discover_skills()
    for skill in skills:
        print(f"- {{skill.name}}: {{skill.description}}")
    
    # 加载技能
    print("\n加载技能...")
    # manager.load_skill("example")
    
    # 列出技能
    print("\n技能列表:")
    skill_list = manager.list_skills()
    for skill_info in skill_list:
        print(f"- {{skill_info['name']}}: {{skill_info['status']}}")
