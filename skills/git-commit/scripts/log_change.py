#!/usr/bin/env python3
"""
AI_CHANGELOG 自动飞行记录仪
==========================
每次代码变更后自动记录变更日志，强制要求风险分析。

Usage (positional):
    python log_change.py <type> <summary> <risk_analysis>

Usage (flags):
    python log_change.py --type <type> --change <summary> --risk <risk_analysis>

Example (positional):
    python log_change.py Feature "Add timeline index optimization" "May affect existing queries performance"

Example (flags):
    python log_change.py --type Feature --change "Add timeline index optimizationMay affect existing queries" --risk " performance"
"""

import sys
import os
import argparse
from datetime import datetime

# 配置
CHANGELOG_FILENAME = "AI_CHANGELOG.md"
CHANGELOG_SUBDIR = "docs"


def find_project_root(start_dir: str = ".") -> str:
    """获取当前 git 仓库的根目录"""
    import subprocess

    try:
        # 使用 git 命令获取仓库根目录
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass

    # git 命令失败时，使用备用方案：向上查找直到 .git 目录
    current = os.path.abspath(start_dir)
    home = os.path.expanduser("~")

    while current != home:
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    # 没找到，返回起始目录
    return start_dir


def get_changelog_path(start_dir=None) -> str:
    """获取 CHANGELOG 文件的完整路径

    Args:
        start_dir: 搜索起点目录，默认为脚本所在目录的父目录
    """
    if start_dir is None:
        # 默认使用脚本所在目录的父目录（支持跨项目使用）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        start_dir = os.path.dirname(script_dir)

    # 首先检查 start_dir
    if os.path.exists(os.path.join(start_dir, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)):
        return os.path.join(start_dir, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)

    # 向上查找项目根目录
    root = find_project_root(start_dir)
    changelog_path = os.path.join(root, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)

    if os.path.exists(changelog_path):
        return changelog_path

    # 文件不存在，返回默认路径（会在追加时创建）
    return os.path.join(root, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)


# 变更类型
CHANGE_TYPES = ["Feature", "Bugfix", "Refactor", "Critical-Fix", "Docs", "Perf"]


def get_change_type_display(change_type: str) -> str:
    """获取变更类型的显示名称"""
    emoji_map = {
        "Feature": "✨",
        "Bugfix": "🐛",
        "Refactor": "♻️",
        "Critical-Fix": "🚨",
        "Docs": "📝",
        "Perf": "⚡",
    }
    emoji = emoji_map.get(change_type, "📦")
    return f"[{change_type}] {emoji}"


def format_entry(change_type: str, summary: str, risk_analysis: str) -> str:
    """格式化日志条目"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    type_display = get_change_type_display(change_type)

    entry = f"""
## [{timestamp}] {type_display}

- **Change**: {summary}
- **Risk Analysis**: {risk_analysis}

---
"""
    return entry


def append_log(
    change_type: str, summary: str, risk_analysis: str, start_dir=None
) -> bool:
    """追加日志到 AI_CHANGELOG.md（ prepend 到文件开头）"""
    # 验证变更类型
    if change_type not in CHANGE_TYPES:
        print(f"❌ Error: Invalid change type '{change_type}'")
        print(f"   Valid types: {', '.join(CHANGE_TYPES)}")
        return False

    # 验证必需参数
    if not summary or not summary.strip():
        print("❌ Error: Summary cannot be empty")
        return False

    if not risk_analysis or not risk_analysis.strip():
        print(
            "❌ Error: Risk analysis cannot be empty - this is the most important field!"
        )
        return False

    # 创建格式化的日志条目
    entry = format_entry(change_type, summary.strip(), risk_analysis.strip())

    # 获取 CHANGELOG 文件路径
    changelog_path = get_changelog_path(start_dir)
    changelog_dir = os.path.dirname(changelog_path)

    try:
        # 确保 docs 目录存在
        if not os.path.exists(changelog_dir):
            os.makedirs(changelog_dir, exist_ok=True)
            print(f"📁 Created directory: {changelog_dir}")

        # 检查文件是否存在
        if os.path.exists(changelog_path):
            # 文件存在：读取现有内容，将新条目 prepend 到开头
            with open(changelog_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # 将新条目 prepend 到文件开头
            new_content = entry + existing_content
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ [Flight Recorder] Prepended entry to {changelog_path}")
        else:
            # 文件不存在：创建新文件
            header = f"""# AI_CHANGELOG

> 自动飞行记录 - 代码变更的唯一真相源
> 自动生成，请勿手动编辑

"""
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(header)
                f.write(entry)
            print(f"✅ [Flight Recorder] Created {changelog_path} with initial entry")

        print(f"   Type: {change_type}")
        print(f"   Summary: {summary}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    # 支持两种调用方式: 位置参数 和 flag 参数
    parser = argparse.ArgumentParser(
        description="AI_CHANGELOG 自动飞行记录仪",
        usage="python log_change.py <type> <summary> <risk_analysis>\n       python log_change.py --type <type> --change <summary> --risk <risk_analysis>",
        add_help=False,
    )
    parser.add_argument(
        "args", nargs="*", help="Positional arguments: type summary risk_analysis"
    )
    parser.add_argument(
        "--type",
        "-t",
        dest="type",
        help="Change type (Feature, Bugfix, Refactor, Critical-Fix, Docs, Perf)",
    )
    parser.add_argument(
        "--change", "-c", dest="change", help="Summary/description of the change"
    )
    parser.add_argument("--risk", "-r", dest="risk", help="Risk analysis")
    parser.add_argument(
        "--dir",
        "-d",
        dest="dir",
        default=None,
        help="Project directory to search for CHANGELOG (defaults to script's parent directory)",
    )
    parser.add_argument(
        "--help", "-h", action="store_true", help="Show this help message"
    )

    # 先检查是否有 --help
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    args = parser.parse_args()

    # 解析参数: 优先使用 flag 参数，其次使用位置参数
    change_type = args.type
    summary = args.change
    risk_analysis = args.risk

    # 如果 flag 参数为空，尝试从位置参数获取
    if not change_type and len(args.args) >= 1:
        change_type = args.args[0]
    if not summary and len(args.args) >= 2:
        summary = args.args[1]
    if not risk_analysis and len(args.args) >= 3:
        risk_analysis = args.args[2]

    # 验证必需参数
    if not change_type or not summary or not risk_analysis:
        print(__doc__)
        print("\n❌ Error: Missing required arguments")
        print("\nPositional usage:")
        print("  python log_change.py Feature 'Your summary' 'Your risk analysis'")
        print("\nFlag usage:")
        print(
            "  python log_change.py --type Feature --change 'Your summary' --risk 'Your risk analysis'"
        )
        sys.exit(1)

    success = append_log(change_type, summary, risk_analysis, args.dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
