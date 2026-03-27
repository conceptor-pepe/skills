# 下游仓库 `AGENTS.md` 写法约定（Go / 獬豸）

> **用途（skills 真源）**：约定「**不双写** `go-code-standards.mdc`」时，`AGENTS.md` 应长什么样。各项目在仓库根 **维护自己的 `AGENTS.md`**，可对照本文裁剪；**禁止**把本文整段当作 `.mdc`（保持 `.mdc` 在 skills 经 `setup.sh` 安装）。

## 原则

1. **流程**：与 `xiezhi-workflow.mdc` 对齐的一段话 + 指向本仓库 `docs/dev/workflow.md`（正文可复制 `cursor/references/repo-workflow-index.md`）。
2. **Go 细则**：只写 **指针**（`go-code-standards.mdc`、`go-audit.mdc`、本仓 `.cursor/rules/code.mdc`），**不**展开与全局重复的条文。
3. **本仓独有**：模块路径、`go.mod` 名、错误码分段、特定 `pkg/` 包名、目录结构、测试示例路径、make 目标等——放在 **「本仓库约定」**。

## 可复制骨架（将 `<...>` 替换为项目实际值）

```markdown
# AGENTS.md - Codebase Guidelines for AI Agents

## AI / Cursor 工作流（与全局规则对齐）

（一段与 xiezhi-workflow 阶段 0–6 对齐的说明 + 0.5 模板路径 `skills/.../task-design-brief.md` + 链接 `docs/dev/workflow.md`）

## Build, Lint, and Test Commands

（仅本仓库：make / go 命令，随项目变）

## Go 编码规范（不双写）

- **细则唯一真源**：`go-code-standards.mdc`、`go-audit.mdc`，由本机 `skills` 经 `setup.sh` 链入 `~/.cursor/rules/`。
- **本仓库指针**：见 [.cursor/rules/code.mdc](.cursor/rules/code.mdc)。
- **禁止**在本文件恢复与上述 `.mdc` 重复的条款（避免漂移）。

## 本仓库约定（补全局未写死的部分）

### 模块路径与 import

- Go module：`<module-name>`（见 `go.mod`）。
- import 第三组：`<module-name>/...`。

### 错误码 / HTTP / 目录 / 测试 / 其他

（仅写本项目与全局不同的约定；能由代码库自解释的用一句「详见 xxx」代替。）
```

## `CLAUDE.md` 配套建议

工作流条款建议缩为一句 **整链** + 强调 **2 / 5 / 6 不得跳过**，避免复述整表。文档同步清单（库表、Swagger、配置等）**按各仓库真实路径** 维护，可参照 `cursor/references/claude-md-hints-for-go-repos.md`。
