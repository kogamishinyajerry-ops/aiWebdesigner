#!/usr/bin/env python3
"""
本地环境安装脚本

将 Skills 和 Agents 系统安装到本地 Python 环境
"""

import os
import sys
import shutil
from pathlib import Path


def setup_local():
    """配置到本地环境"""
    
    print("=" * 60)
    print("配置 Skills 和 Agents 系统到本地环境")
    print("=" * 60)
    
    # 获取脚本所在目录
    workspace = Path(__file__).parent
    
    # 1. 创建本地安装目录
    print("\n1. 创建本地安装目录...")
    local_install_dir = Path.home() / ".codebuddy_skills_agents"
    local_install_dir.mkdir(exist_ok=True)
    print(f"   ✓ 本地安装目录: {local_install_dir}")
    
    # 2. 复制 skills 目录
    print("\n2. 复制 Skills 系统...")
    skills_dest = local_install_dir / "skills"
    if skills_dest.exists():
        shutil.rmtree(skills_dest)
    shutil.copytree(workspace / "skills", skills_dest)
    print(f"   ✓ Skills 已复制到: {skills_dest}")
    
    # 3. 复制 agents 目录
    print("\n3. 复制 Agents 系统...")
    agents_dest = local_install_dir / "agents"
    if agents_dest.exists():
        shutil.rmtree(agents_dest)
    shutil.copytree(workspace / "agents", agents_dest)
    print(f"   ✓ Agents 已复制到: {agents_dest}")
    
    # 4. 复制管理工具
    print("\n4. 复制管理工具...")
    manager_dest = local_install_dir / "skills_manager.py"
    shutil.copy2(workspace / "skills_manager.py", manager_dest)
    print(f"   ✓ 管理工具已复制到: {manager_dest}")
    
    # 5. 创建本地入口脚本
    print("\n5. 创建入口脚本...")
    entry_script = local_install_dir / "sa.py"
    entry_script.write_text("""#!/usr/bin/env python3
import sys
from pathlib import Path

# 添加到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入并执行管理工具
from skills_manager import main

if __name__ == "__main__":
    main()
""")
    entry_script.chmod(0o755)
    print(f"   ✓ 入口脚本已创建: {entry_script}")
    
    # 6. 创建便捷命令脚本
    print("\n6. 创建便捷命令...")
    
    # 检测 shell 类型
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        shell_config = Path.home() / '.zshrc'
    elif 'bash' in shell:
        shell_config = Path.home() / '.bashrc'
    else:
        shell_config = Path.home() / '.bash_profile'
    
    # 创建 bin 目录
    bin_dir = Path.home() / "bin"
    bin_dir.mkdir(exist_ok=True)
    
    # 创建便捷命令
    cmd_script = bin_dir / "sa"
    cmd_script.write_text(f"""#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, "{local_install_dir}")
exec(open("{local_install_dir}/sa.py").read())
""")
    cmd_script.chmod(0o755)
    print(f"   ✓ 便捷命令已创建: {cmd_script}")
    
    # 7. 更新 shell 配置
    print("\n7. 更新 shell 配置...")
    bin_path_str = str(bin_dir)
    
    if shell_config.exists():
        with open(shell_config, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if f'export PATH="$PATH:{bin_path_str}"' not in content:
            with open(shell_config, 'a', encoding='utf-8') as f:
                f.write(f'\n# Skills and Agents 系统\nexport PATH="$PATH:{bin_path_str}"\n')
            print(f"   ✓ 已更新 {shell_config}")
        else:
            print(f"   ✓ PATH 已配置")
    else:
        print(f"   ⚠ 未找到 {shell_config.name}")
    
    # 8. 创建 Python 包安装脚本
    print("\n8. 创建 Python 包...")
    
    setup_py = workspace / "setup.py"
    setup_py.write_text(f"""
from setuptools import setup, find_packages

setup(
    name="codebuddy-skills-agents",
    version="1.0.0",
    description="Skills and Agents 系统 - 对标 Claude Code",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
)
""")
    
    print(f"   ✓ setup.py 已创建")
    
    # 9. 显示配置完成信息
    print("\n" + "=" * 60)
    print("配置完成！")
    print("=" * 60)
    
    print("\n📦 安装位置:")
    print(f"   {local_install_dir}")
    
    print("\n🎯 使用方式:")
    print("\n   方式 1: 使用便捷命令 (需要重启 shell)")
    print("   sa --list-skills              # 列出技能")
    print("   sa --list-agents              # 列出代理")
    print("   sa --interactive              # 交互模式")
    
    print("\n   方式 2: 直接运行脚本")
    print(f"   python {entry_script} --list-skills")
    
    print("\n   方式 3: 在 Python 代码中使用")
    print("   from skills import get_skill_manager")
    print("   from agents import get_orchestrator")
    
    print("\n⚠️  重要提示:")
    print(f"   请在新的终端中执行以下命令使配置生效:")
    print(f"   source {shell_config}")
    print(f"   或者")
    print(f"   export PATH=\"$PATH:{bin_path_str}\"")
    
    print("\n✅ 安装可选项:")
    print("   如果希望将系统作为 Python 包安装:")
    print("   cd /workspace && pip install -e .")
    
    return True


def create_setup_py():
    """创建可编辑安装的 setup.py"""
    
    workspace = Path(__file__).parent
    
    setup_content = """
from setuptools import setup, find_packages

setup(
    name="codebuddy-skills-agents",
    version="1.0.0",
    description="Skills and Agents 系统 - 对标 Claude Code",
    long_description=open('README_SKILLS_AGENTS.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
"""
    
    setup_file = workspace / "setup.py"
    setup_file.write_text(setup_content)
    print(f"✓ setup.py 已创建: {setup_file}")
    
    return True


if __name__ == "__main__":
    try:
        setup_local()
        print("\n" + "=" * 60)
        print("安装脚本运行完成！")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 安装失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
