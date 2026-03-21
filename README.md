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

## Kiro 使用说明

Kiro 的 skills/hooks/steering 是三套独立机制，通过本仓库的 symlink 管理，无需额外安装命令。

### Skills（`kiro/skills/`）

手动调用型，在 Kiro 对话中说出触发词即可启动：

| Skill | 触发方式 | 说明 |
|-------|---------|------|
| `go-complete-review` | 「完整代码审查」「代码 review」 | 依次执行 audit.py + 测试功能 Review |
| `test-functionality-review` | 「测试功能 review」「测试用例设计」 | 设计测试用例并评审代码 |

### Hooks（`kiro/hooks/`）

**自动触发**，无需手动调用，Kiro 会在特定事件时执行：

| Hook | 触发时机 | 是否启用 | 说明 |
|------|---------|---------|------|
| `auto-change-summary` | agent 完成后（agentStop） | ✅ | 自动生成本次会话的变更报告 |
| `go-pre-write-check` | 写入文件前（preToolUse/write） | ✅ | Go 文件写入前自检 5 项编码规范 |
| `go-code-review` | 编辑 .go 文件时（fileEdited） | ❌ 已禁用 | 已被 go-pre-write-check 替代 |

> 启用/禁用 hook：修改对应 `.kiro.hook` 文件中的 `"enabled"` 字段即可，改动会实时生效。

### Steering（`kiro/steering/`）

**始终生效**（`inclusion: always`），会自动注入到每次对话上下文中，相当于 Kiro 版的 always-apply 规则：

| 文件 | 说明 |
|------|------|
| `code.md` | Go 代码编写规范 |
| `commit-summary.md` | Commit 变更总结格式规范 |
| `test-functionality-review.md` | Code Review 后强制执行测试功能 Review |

> Steering 文件的 `inclusion` 字段可选 `always`（始终）或 `manual`（手动触发）。

---

## 更新 skill

直接编辑 repo 目录内的文件，因为原工具路径已是 symlink，修改即时生效，`git commit` 后推送即可同步到其他机器。

## 添加新 skill

1. 在对应工具子目录（如 `cursor/skills/<name>/`）创建 `SKILL.md`
2. 在本机对应工具目录手动建 symlink：`ln -sfn ~/project/skills/cursor/skills/<name> ~/.cursor/skills/<name>`
3. 在 `setup.sh` 中按需补充（如果是遵循通用目录扫描规则则无需改动）
4. `git add -A && git commit && git push`
