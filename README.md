# Claude Plugins Marketplace

## 安装

```bash
# 添加 Marketplace
/plugin marketplace add AdolphKevin/claude-plugins

# 安装插件
/plugin install git-commit@claude-plugins
```

## 安装后设置

由于 `log_change.py` 脚本需要从命令行调用，安装插件后需要创建软链接以便全局使用：

```bash
# 创建软链接（只需执行一次）
mkdir -p ~/.claude/skills
ln -sf ~/.claude/plugins/cache/claude-plugins/plugins/git-commit/skills/git-commit/scripts/log_change.py ~/.claude/skills/log_change.py
```

或者直接在命令中使用完整路径：

```bash
python ~/.claude/plugins/cache/claude-plugins/plugins/git-commit/skills/git-commit/scripts/log_change.py <type> <summary> <risk_analysis>
```

## 更新插件

```bash
/plugin update git-commit@claude-plugins
```
