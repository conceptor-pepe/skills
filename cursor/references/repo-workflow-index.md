# 开发与 AI 协作流程索引

> **用途（skills 真源）**：本文件为 **下游 Go 仓库** `docs/dev/workflow.md` 的推荐正文。请 **整份复制** 到目标仓库该路径；文中相对链接以 **文件位于 `docs/dev/`** 为准。

本仓库在启用 Cursor 全局规则时，**端到端顺序**以 **`xiezhi-workflow.mdc`（獬豸工作流）** 为**唯一真源**（通常 `~/.cursor/rules/`，由本机 **`skills`** 仓库 `setup.sh` 同步）。

## 自动触发

以下文件在全局规则目录中为 **`alwaysApply: true`**：Cursor **每次对话自动注入**，无需 `@`，用于自动拉起工作流与门禁（详见 `xiezhi-workflow.mdc` 文首列表）：

- `xiezhi-workflow.mdc`、`task-design-brief-gate.mdc`（**阶段 0.5 硬门禁**）、`go-code-standards.mdc`、`go-audit.mdc`、`test-functionality-review.mdc`、`commit-summary.mdc`、`module-review-gates.mdc`、`feature-planning-files.mdc`

## 阶段速览

| 阶段 | 含义 | 单一真源 |
|------|------|----------|
| 0 | 功能启动（PRD、task_plan、`docs/features/<name>/`） | **`xiezhi-workflow.mdc`「阶段 0」** + **`feature-planning-files.mdc`** |
| 0.5 | 方案简报（四步设计） | **`task-design-brief-gate.mdc`**（自动注入）+ **`skills/cursor/references/task-design-brief.md`**（模板，须 Read） |
| 1–6 | 编码、审计、模块 Gate、CR、测试评审、提交总结 | 各全局 `.mdc` 及 SKILL（见 `xiezhi-workflow.mdc` 阶段表） |

## 仓库内必读

- [AGENTS.md](../AGENTS.md)（命令与本仓约定；**Go 编码细则不重复**，以全局 `go-code-standards.mdc` 为准）
- [CLAUDE.md](../CLAUDE.md)
- [.cursor/rules/code.mdc](../.cursor/rules/code.mdc)（指向全局规范，不重复正文）

## 安装 / 更新

```bash
cd ~/project/skills && bash setup.sh
```

已删除的重复规则：**`feature-start-workflow.mdc`**、**`task-design-brief.mdc`** 内容已并入 **`xiezhi-workflow.mdc`** 与 **`cursor/references/task-design-brief.md`**。若本机仍存在上述 symlink，请删除后重跑 `setup.sh`。弃用的 **`macrode-workflow.mdc`** symlink 亦应删除。
