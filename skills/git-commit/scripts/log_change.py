#!/usr/bin/env python3
"""
AI_CHANGELOG 自动飞行记录仪
==========================
每次代码变更后自动记录变更日志，强制要求风险分析。

Usage:
    python log_change.py <type> <summary> <risk_analysis>

Example:
    python log_change.py Feature "Add timeline index optimization" "May affect existing queries performance"
"""
import sys
import os
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
            timeout=5
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


def get_changelog_path() -> str:
    """获取 CHANGELOG 文件的完整路径"""
    # 首先检查当前目录
    current_dir = "."
    if os.path.exists(os.path.join(current_dir, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)):
        return os.path.join(current_dir, CHANGELOG_SUBDIR, CHANGELOG_FILENAME)

    # 向上查找项目根目录
    root = find_project_root(current_dir)
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
        "Perf": "⚡"
    }
    emoji = emoji_map.get(change_type, "📦")
    return f"[{change_type}] {emoji}"


def format_entry(change_type: str, summary: str, risk_analysis: str) -> str:
    """格式化日志条目"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    type_display = get_change_type_display(change_type)

    entry = f"""
## [{timestamp}] {type_display}

- **Change**: {summary}
- **Risk Analysis**: {risk_analysis}

---
"""
    return entry


def append_log(change_type: str, summary: str, risk_analysis: str) -> bool:
    """追加日志到 AI_CHANGELOG.md"""
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
        print("❌ Error: Risk analysis cannot be empty - this is the most important field!")
        return False

    # 创建格式化的日志条目
    entry = format_entry(change_type, summary.strip(), risk_analysis.strip())

    # 获取 CHANGELOG 文件路径
    changelog_path = get_changelog_path()
    changelog_dir = os.path.dirname(changelog_path)

    # 追加到文件
    try:
        # 确保 docs 目录存在
        if not os.path.exists(changelog_dir):
            os.makedirs(changelog_dir, exist_ok=True)
            print(f"📁 Created directory: {changelog_dir}")

        with open(changelog_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"✅ [Flight Recorder] Log appended to {changelog_path}")
        print(f"   Type: {change_type}")
        print(f"   Summary: {summary}")
        return True
    except FileNotFoundError:
        # 文件不存在，创建新文件
        header = f"""# AI_CHANGELOG

> 自动飞行记录 - 代码变更的唯一真相源
> 自动生成，请勿手动编辑

"""
        try:
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(header)
                f.write(entry)
            print(f"✅ [Flight Recorder] Created {changelog_path} with initial entry")
            return True
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False
    except Exception as e:
        print(f"❌ Error appending log: {e}")
        return False


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print("\nExample:")
        print("  python log_change.py Feature 'Add message handler' 'May affect existing API responses'")
        sys.exit(1)

    change_type = sys.argv[1]
    summary = sys.argv[2]
    risk_analysis = sys.argv[3]

    success = append_log(change_type, summary, risk_analysis)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
