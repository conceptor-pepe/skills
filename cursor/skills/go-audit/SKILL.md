---
name: go-audit
description: Go 编码规范自动审计。在完成任何 Go 代码修改后，必须自动执行 audit.py 脚本进行编码规范检查。Use proactively after any Go code changes — do NOT wait for user to ask. Also use when the user explicitly requests a coding standards check.
---

# Go 编码规范自动审计

## 触发时机（自动，无需用户要求）

以下场景 **必须自动执行**，不等待用户指令：
- 完成任何 `.go` 文件的新增或修改后
- 完成一个 commit/task 的所有代码修改后（输出总结前）
- 用户显式要求编码规范检查时

## 使用方法

### 审计指定文件

```bash
python3 ~/.cursor/skills/go-audit/scripts/audit.py <file1.go> [file2.go ...]
```

### 审计整个目录

```bash
python3 ~/.cursor/skills/go-audit/scripts/audit.py --dir <directory>
```

### 详细输出（显示所有违规明细）

```bash
python3 ~/.cursor/skills/go-audit/scripts/audit.py --dir <directory> -v
```

## 检查项（11 项）

| # | 检查项 | 规则 |
|---|--------|------|
| 1 | 公开函数注释 | 所有首字母大写的函数必须有 `//` Go doc 注释 |
| 2 | 函数长度 | 单个函数不超过 50 行 |
| 3 | 函数参数 | 参数个数不超过 5 个，超过应使用结构体封装 |
| 4 | 嵌套深度 | if/for/switch 嵌套不超过 2 层（Gin 中间件允许 3 层） |
| 5 | 错误处理 | `_ =` 忽略错误必须有 `//` 注释说明原因 |
| 6 | 错误分支日志 | 错误分支退出前必须记录日志；**service 层禁止使用 `audit:allow-no-log`**，仅 handler/repository 层可豁免 |
| 7 | 无反射 | 不使用 `reflect` 包，除非绝对必要 |
| 8 | context 传递 | 涉及 DB/HTTP/RPC 的公开函数须接受 `context.Context` |
| 9 | 接口最小化 | 接口方法数不超过 10 个 |
| 10 | int64 精度保护 | int64 字段 json tag 必须含 `,string`；`[]int64` 必须替换为 `[]types.StringID` |
| 11 | 写操作成功日志 | service/handler 关键写操作在成功出口必须有 `Info` 日志（支持 `audit:allow-no-success-log` 豁免高频幂等场景） |

## 输出格式

- **全部通过**: `编码规范审计 ✅ (11/11)`
- **有违规**: `编码规范审计 ❌ (N/11)` + 逐条违规明细（文件:行号 [规则] 描述）
- **退出码**: 0 = 全部通过，1 = 有违规

## 工作流集成

1. 完成代码修改后，对修改的文件运行审计
2. 如有违规，**先修复**再继续
3. 全部通过后，在 commit 总结中追加 `编码规范审计 ✅ (11/11)`

## `audit:allow-no-log` 使用规范

`audit:allow-no-log` 是错误分支日志检查的行内豁免标记，**必须按层级严格管控**：

| 层级 | 是否允许 | 典型场景 |
|------|----------|----------|
| **service** | **禁止** | 所有错误分支必须有日志（Error/Warn/Info），确保问题可追溯 |
| handler | 允许 | DTO 绑定失败、鉴权缺失等高频预期错误，由框架统一处理 |
| repository | 允许 | 错误向上传播，由 service 层统一记录日志 |

**service 层日志级别选择**：
- `Error`：系统/基础设施故障（DB 失败、Redis 失败、加密失败）
- `Warn`：业务拒绝或安全事件（密码错误、账号禁用、限流触发、跨域 Token）
- `Info`：正常放行路径中的 err 分支（如 Redis key 不存在代表无限流记录）

## `audit:allow-no-success-log` 使用规范

`audit:allow-no-success-log` 是关键写操作成功日志检查的豁免标记，仅用于明确高频或幂等场景（如批量重试、补偿任务）。

| 层级 | 是否允许 | 说明 |
|------|----------|------|
| service | 允许（受限） | 必须在函数体内写明豁免原因注释，禁止默认滥用 |
| handler | 允许（受限） | 仅用于网关级高频入口，需保证链路其他层可追踪 |
| repository | 不适用 | 成功日志规则仅检查 service/handler |

## 智能排除

脚本自动排除以下情况，避免误报：
- `_test.go` 测试文件
- `vendor/` 目录
- `New...` 构造函数的 context 检查（构造阶段通常不执行 I/O）
- `*gin.Context` 参数的 Gin handler（通过 `c.Request.Context()` 间接获取）
- 返回 `*gorm.DB` 的 scope/builder 函数
- Gin 中间件的外层闭包（嵌套阈值放宽为 3 层）
