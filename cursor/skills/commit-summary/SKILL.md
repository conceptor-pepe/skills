---
name: commit-summary
description: Generate structured commit summaries as clickable two-column tables. Use after completing code changes for a commit, before presenting results to the user, or when summarizing modifications.
---

# Commit Summary Format

After completing all changes for a commit/task, present the summary using the structured format below.

## Output Format

### 1. Header

```
**Commit N: <标题>** 已完成。
```

### 2. Changes Table

Two columns only: **文件** and **变更说明**. Each row is one file.

```markdown
| 文件 | 变更说明 |
|------|----------|
| [config.yaml](skild-art-backend/configs/config.yaml) | 新增 agent 配置段 |
| [jwt.go](skild-art-backend/internal/infra/auth/jwt.go) | Claims 增加 TokenType 字段 |
```

#### File path format — critical for Cursor navigation

Use `[filename](workspace-relative-path)`:
- **Display text**: filename only (e.g. `jwt.go`)
- **Link path**: path relative to **workspace root** (the directory containing `.cursor/`), NOT relative to the Go module or package root

```
✅ [jwt.go](skild-art-backend/internal/infra/auth/jwt.go)
❌ `internal/infra/auth/jwt.go`   ← relative to module root, Cursor cannot resolve
❌ [jwt.go](internal/infra/auth/jwt.go)  ← same problem
```

To find the workspace root: it is the directory where `.cursor/` lives.
In this project: workspace root = `/home/con/project/skildart`, Go module is inside `skild-art-backend/`, so all backend paths must be prefixed with `skild-art-backend/`.

#### Description rules

- **≤ 20 characters** — one short action phrase only
- No full sentences, no conjunctions

### 3. Key Points Section

```markdown
**关键设计点**：
- Point 1
- Point 2

**验证结果**：编译通过 ✅ | 测试通过 ✅ | Lint 清洁 ✅ | 编码规范审计 ✅ (N/N)
```

Only list items that actually apply. Mark failed checks with ❌.

### 4. Commit Message

```markdown
**提交信息**：
\`\`\`
feat(scope): 简要标题

- 变更点1
- 变更点2
\`\`\`
```

Rules:
- First line: conventional commit format `feat/fix/refactor(scope): title`
- Body: `-` list of changes, one per line
- Language consistent with project (Chinese project → Chinese)

## Full Example

**Commit 2: JWT Claims 扩展** 已完成。

| 文件 | 变更说明 |
|------|----------|
| [jwt.go](skild-art-backend/internal/infra/auth/jwt.go) | Claims 增加 TokenType 字段 |
| [auth.go](skild-art-backend/internal/domain/admin/service/auth.go) | 登录传入 TokenTypeAdmin |
| [jwt_property_test.go](skild-art-backend/tests/property/jwt_property_test.go) | 补传 tokenType + 断言 |

**关键设计点**：
- 向后兼容：`ParseToken` 对空 `token_type` 旧 token 默认填充 `"merchant"`

**验证结果**：编译通过 ✅ | 测试通过 (5/5) ✅ | 编码规范审计 ✅ (9/9)

**提交信息**：
```
feat(auth): JWT Claims 扩展支持 TokenType

- Claims 新增 TokenType 字段，GenerateToken 增加第 4 参数
- Admin/Merchant 登录调用传入对应 TokenType 常量
- 测试补传 tokenType 并增加一致性断言
```
