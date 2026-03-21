# Skills

本仓库统一管理所有 AI 工具（Cursor / Kiro / Claude / Codex）的自定义 Skills、Rules 和 Hooks。

## 目录结构

```
skills/
├── setup.sh
├── cursor/
│   ├── skills/          → ~/.cursor/skills/
│   ├── skills-cursor/   → ~/.cursor/skills-cursor/
│   └── rules/           → ~/.cursor/rules/*.mdc
├── codex/
│   └── skills/          → ~/.codex/skills/
├── kiro/
│   ├── skills/          → ~/.kiro/skills/
│   ├── hooks/           → ~/.kiro/hooks/
│   └── steering/        → ~/.kiro/steering/
└── claude/
    └── skills/          → ~/.claude/skills/
```

> `pretty-mermaid` 统一存放在 `cursor/skills/pretty-mermaid/`，其他工具路径通过 `setup.sh` 建 symlink 指向这里，避免重复维护。

---

## 新机器安装

### 第一步：clone 并建 symlink

```bash
git clone git@github.com:conceptor-pepe/skills.git ~/project/skills
cd ~/project/skills
bash setup.sh
```

### 第二步：安装 Claude 插件（见下方 Claude 章节）

---

## Cursor

### Skills（`cursor/skills/`）

在对话中说出触发词，Cursor Agent 会自动读取并执行对应 skill。

| Skill | 触发词 / 使用时机 | 说明 |
|-------|-----------------|------|
| `go-audit` | Go 文件修改后自动执行 | 运行 `audit.py` 对 `.go` 文件做 9 项编码规范检查 |
| `go-code-standards` | 编写 Go 代码时 | Go 代码规范与最佳实践参考 |
| `coding-standards-enforcer` | 进行 Go 代码改动、重构时 | 改动前强制要求读取规范 |
| `test-functionality-review` | Code Review 完成后自动执行 | 设计测试用例并从测试角度评审代码 |
| `commit-summary` | 完成一次代码改动后 | 生成结构化、带超链接的 commit 变更总结 |
| `grill-me` | 「质疑我的方案」「压力测试」「grill me」 | 对设计方案进行无死角追问，找漏洞 |
| `improve-codebase-architecture` | 「架构改进」「重构机会」「找耦合问题」 | 探索代码库，识别浅层模块和紧耦合，产出 RFC |
| `planning-with-files` | 「写计划」，复杂多步骤任务开始时 | 文件式任务规划（task_plan.md / findings.md） |
| `prd-to-plan` | 「PRD 转计划」「垂直切片」 | 将 PRD 拆解为分阶段实施计划 |
| `write-a-prd` | 「写 PRD」「产品需求」 | 通过访谈 + 代码探索创建 PRD 文档 |
| `frontend-design` | 构建前端组件、页面、应用时 | 生成高质量、有设计感的前端界面代码 |
| `pretty-mermaid` | 「渲染 Mermaid 图」「创建流程图」 | 渲染美观的 Mermaid 图（SVG / ASCII，多主题） |

### Skills-Cursor（`cursor/skills-cursor/`）

Cursor 工具类 skill，用于管理 Cursor 自身的配置：

| Skill | 触发词 / 使用时机 | 说明 |
|-------|-----------------|------|
| `create-rule` | 「创建规则」「添加编码规范」 | 创建 `.cursor/rules/*.mdc` 持久规则 |
| `create-skill` | 「创建 skill」「写 SKILL.md」 | 创建新的 Agent Skill |
| `create-subagent` | 「创建子代理」 | 创建专用子代理 |
| `migrate-to-skills` | 「迁移 rules 到 skills」 | 将 alwaysApply 规则迁移为 skill |
| `update-cursor-settings` | 「修改编辑器设置」 | 修改 `settings.json` |

### Rules（`cursor/rules/`）

全部为 `alwaysApply: true`，每次对话自动注入，无需手动触发：

| 规则 | 说明 |
|------|------|
| `go-code-standards.mdc` | Go 代码编写规范（强制，编写前必须遵守） |
| `go-audit.mdc` | 修改 `.go` 文件后自动执行 `audit.py` 审计 |
| `xiezhi-workflow.mdc` | 獬豸工作流：编写 → 审计 → Review → 测试评审 → 提交总结 |
| `test-functionality-review.mdc` | Code Review 完成后必须立即执行测试功能 Review |
| `commit-summary.mdc` | 每次 commit 完成后按统一格式输出变更总结 |
| `module-review-gates.mdc` | 模块级审计按 Gate 0→4 顺序执行 |

---

## Kiro

### Skills（`kiro/skills/`）

手动触发，在对话中说出触发词启动：

| Skill | 触发词 | 说明 |
|-------|-------|------|
| `go-complete-review` | 「完整代码审查」「代码 review」 | 依次执行 audit.py + 测试功能 Review |
| `test-functionality-review` | 「测试功能 review」「测试用例设计」 | 设计测试用例并评审代码 |

### Hooks（`kiro/hooks/`）

事件驱动，自动触发，无需手动调用：

| Hook | 触发事件 | 是否启用 | 说明 |
|------|---------|---------|------|
| `auto-change-summary` | agent 完成后（agentStop） | ✅ | 自动生成本次会话变更报告 |
| `go-pre-write-check` | 写入文件前（preToolUse/write） | ✅ | Go 文件写入前自检 5 项编码规范 |
| `go-code-review` | 编辑 .go 文件时（fileEdited） | ❌ 已禁用 | 已被 go-pre-write-check 替代 |

> 修改 `.kiro.hook` 文件中的 `"enabled"` 字段即可启用/禁用，实时生效。

### Steering（`kiro/steering/`）

`inclusion: always`，始终注入上下文，相当于 Kiro 版的 alwaysApply 规则：

| 文件 | 说明 |
|------|------|
| `code.md` | Go 代码编写规范 |
| `commit-summary.md` | Commit 变更总结格式规范 |
| `test-functionality-review.md` | Code Review 后强制执行测试功能 Review |

---

## Claude

### Skills（`claude/skills/`）

本仓库管理的手动 skill（通过 symlink 挂载到 `~/.claude/skills/`）：

| Skill | 触发词 | 说明 |
|-------|-------|------|
| `pretty-mermaid` | 「渲染 Mermaid 图」「创建流程图」 | 渲染美观的 Mermaid 图 |

### 插件（通过 Claude 内置插件系统管理）

Claude 的大部分 skill 通过插件机制安装，新机器需在 Claude Code 中重新安装。

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

| 插件 | 来源 | Skill 数量 | 说明 |
|------|------|-----------|------|
| `gopls-lsp` | anthropics/claude-plugins-official | — | Go 语言 LSP 支持 |
| `code-review` | anthropics/claude-plugins-official | — | 代码审查工具 |
| `context7` | anthropics/claude-plugins-official | — | 库文档实时查询 |
| `superpowers` | obra/superpowers-marketplace | 13 | 完整开发工作流（TDD、调试、计划、分支管理等） |
| `obsidian` | kepano/obsidian-skills | 5 | Obsidian 笔记操作（defuddle、json-canvas、obsidian-cli 等） |
| `claude-hud` | jarrodwatts/claude-hud | — | context 用量 / 工具 / agent 状态可视化（项目级） |

---

## Codex

### Skills（`codex/skills/`）

通过 symlink 挂载到 `~/.codex/skills/`：

| Skill | 触发词 | 说明 |
|-------|-------|------|
| `xiezhi-go` | Go 代码任务时自动使用 | 在 Codex 中使用 Cursor 的 Go 编码规范 + go-audit 审计流程 |

> Codex 的 `.system/` 目录（skill-installer、skill-creator、openai-docs）为系统内置 skill，不纳入本仓库。

---

## 更新 skill

直接编辑 repo 目录内的文件。由于本机路径已是 symlink，修改即时生效，`git commit && git push` 后即可同步到其他机器。

## 添加新 skill

1. 在对应工具子目录创建 `SKILL.md`（如 `cursor/skills/<name>/SKILL.md`）
2. 本机手动建 symlink：`ln -sfn ~/project/skills/cursor/skills/<name> ~/.cursor/skills/<name>`
3. 若需要在多个工具中共用，在 `setup.sh` 中补充额外 symlink 逻辑
4. `git add -A && git commit && git push`
