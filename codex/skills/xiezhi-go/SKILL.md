---
name: xiezhi-go
description: 使用 Cursor 的獬豸（Xiezhi）工作流、Go 编码规范和 go-audit 审计处理 Go 代码任务。
---

# Xiezhi Go Workflow（獬豸）

## Read First
Before modifying Go code, read and follow these sources:
- `/home/con/.cursor/rules/xiezhi-workflow.mdc`（端到端顺序）
- `/home/con/.cursor/rules/task-design-brief-gate.mdc`（阶段 0.5 必须执行/豁免条件）
- `skills` 仓库 `cursor/references/task-design-brief.md`（0.5 四步模板，须 Read）
- `/home/con/.cursor/rules/go-code-standards.mdc`
- `/home/con/.cursor/skills/go-code-standards/SKILL.md`
- `/home/con/.cursor/rules/go-audit.mdc`
- `/home/con/.cursor/skills/go-audit/SKILL.md`

## Implementation Rules
- Use the Cursor Go coding standards as the primary style and quality baseline
- Keep functions small, use early returns, and avoid deep nesting
- Public functions must include Go doc comments with `@param` and `@return`
- Handle all errors explicitly and prefer contextual wrapping
- Use structured logging for non-high-frequency error branches

## Mandatory Audit
After modifying any `.go` files, run:
`python3 /home/con/.cursor/skills/go-audit/scripts/audit.py <modified-go-files>`

If the audit fails:
- fix all violations
- rerun the audit until it passes

## Final Reporting
Include the audit result in the final response, for example:
- `编码规范审计 ✅ (11/11)`

## Usage
Use this skill for any Go code task in repositories that adopt the **Xiezhi / 獬豸** workflow (`xiezhi-workflow.mdc`).
