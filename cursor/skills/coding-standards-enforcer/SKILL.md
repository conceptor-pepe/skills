---
name: coding-standards-enforcer
description: Enforce Go coding standards by requiring rule review before edits. Use when performing Go code changes, refactors, or any task that touches .go files.
---

# Coding Standards Enforcer

## Quick Start
在开始任何 Go 代码修改前，先执行以下检查：
1. 读取仓库内 `.cursor/rules/team-coding-standards.mdc`
2. 读取 `AGENTS.md` 中的强制要求
3. 在实现前用 2-3 句总结关键约束（函数长度、单一职责、错误处理等）

## Workflow
1. **发现规则**：优先使用项目内规则（`.cursor/rules/team-coding-standards.mdc`）
2. **缺省策略**：若未找到该规则，读取 `AGENTS.md` 并遵守其中的 Go 规范
3. **执行约束**：实现过程中持续检查是否违反函数长度、职责边界、错误处理和模块依赖
4. **交付说明**：完成后明确说明测试建议与风险点

## Non-negotiables
- 禁止跳过错误处理或吞错
- 禁止破坏性 git 操作，除非用户明确授权
- 不得忽略团队规则或声称已遵守但未实际执行
