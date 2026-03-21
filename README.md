# skills

本仓库统一管理所有 AI 工具（Cursor / Kiro / Claude / Codex）的自定义 Skills、Rules 和 Hooks。

## 目录结构

```
skills/
├── setup.sh                    # 一键安装脚本
├── cursor/
│   ├── skills/                 # → ~/.cursor/skills/
│   ├── skills-cursor/          # → ~/.cursor/skills-cursor/
│   └── rules/                  # → ~/.cursor/rules/*.mdc
├── codex/
│   └── skills/                 # → ~/.codex/skills/
├── kiro/
│   ├── skills/                 # → ~/.kiro/skills/
│   ├── hooks/                  # → ~/.kiro/hooks/
│   └── steering/               # → ~/.kiro/steering/
└── claude/
    └── skills/                 # → ~/.claude/skills/
```

> `pretty-mermaid` 统一存放在 `cursor/skills/pretty-mermaid/`，其他工具的路径通过 `setup.sh` 建 symlink 指向这里，避免内容重复。

## 新机器安装

### 第一步：clone 并建 symlink

```bash
git clone git@github.com:conceptor-pepe/skills.git ~/project/skills
cd ~/project/skills
bash setup.sh
```

执行后所有工具目录里会建好 symlink，重启对应工具即可生效。

### 第二步：安装 Claude 插件

Claude 的插件通过内置插件系统管理，不存入本仓库，需在 Claude Code 里重新安装。

#### 注册 Marketplace

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin marketplace add obra/superpowers-marketplace
/plugin marketplace add kepano/obsidian-skills
/plugin marketplace add jarrodwatts/claude-hud
```

#### 安装插件

```
/plugin install gopls-lsp@claude-plugins-official
/plugin install code-review@claude-plugins-official
/plugin install context7@claude-plugins-official
/plugin install superpowers@superpowers-marketplace
/plugin install obsidian@obsidian-skills
```

> `claude-hud` 是项目级插件，在需要使用的项目目录里执行：
> ```
> /plugin marketplace add jarrodwatts/claude-hud
> /plugin install claude-hud@claude-hud
> ```

#### 已安装插件说明

| 插件 | 来源 | 说明 |
|------|------|------|
| `gopls-lsp` | anthropics/claude-plugins-official | Go 语言 LSP 支持 |
| `code-review` | anthropics/claude-plugins-official | 代码审查工具 |
| `context7` | anthropics/claude-plugins-official | 库文档实时查询 |
| `superpowers` | obra/superpowers-marketplace | 完整开发工作流（13 个 skill，含 TDD、调试、计划等） |
| `obsidian` | kepano/obsidian-skills | Obsidian 笔记操作（5 个 skill） |
| `claude-hud` | jarrodwatts/claude-hud | context 用量 / 工具 / agent 可视化 HUD（项目级） |

## 更新 skill

直接编辑 repo 目录内的文件，因为原工具路径已是 symlink，修改即时生效，`git commit` 后推送即可同步到其他机器。

## 添加新 skill

1. 在对应工具子目录（如 `cursor/skills/<name>/`）创建 `SKILL.md`
2. 在本机对应工具目录手动建 symlink：`ln -sfn ~/project/skills/cursor/skills/<name> ~/.cursor/skills/<name>`
3. 在 `setup.sh` 中按需补充（如果是遵循通用目录扫描规则则无需改动）
4. `git add -A && git commit && git push`
