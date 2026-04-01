---
inclusion: always
globs: "**/*.go"
---

# Go 编码规范自动审计

## 触发时机（主动执行）

以下场景**应该主动执行审计**：
- 完成任何 `.go` 文件的新增或修改后
- 完成一个 commit/task 的所有代码修改后（输出总结前）
- 用户显式要求编码规范检查时

## 审计脚本位置

```bash
~/.kiro/skills/go-audit/scripts/audit.py
```

## 使用方式

### 审计指定文件
```bash
python3 ~/.kiro/skills/go-audit/scripts/audit.py <file1.go> [file2.go ...]
```

### 审计整个目录
```bash
python3 ~/.kiro/skills/go-audit/scripts/audit.py --dir <directory>
```

### 详细输出（显示所有违规明细）
```bash
python3 ~/.kiro/skills/go-audit/scripts/audit.py --dir <directory> -v
```

## 检查项（9 项）

| # | 检查项 | 规则 |
|---|--------|------|
| 1 | 公开函数注释 | 所有首字母大写的函数必须有 `//` Go doc 注释 |
| 2 | 函数长度 | 单个函数不超过 50 行 |
| 3 | 函数参数 | 参数个数不超过 5 个，超过应使用结构体封装 |
| 4 | 嵌套深度 | if/for/switch 嵌套不超过 2 层（Gin 中间件允许 3 层） |
| 5 | 错误处理 | `_ =` 忽略错误必须有 `//` 注释说明原因 |
| 6 | 错误分支日志 | 非高频错误分支退出前必须记录日志（可用 `audit:allow-no-log` 豁免） |
| 7 | 无反射 | 不使用 `reflect` 包，除非绝对必要 |
| 8 | context 传递 | 涉及 DB/HTTP/RPC 的公开函数须接受 `context.Context` |
| 9 | 接口最小化 | 接口方法数不超过 10 个 |

## 输出格式

- **全部通过**: `编码规范审计 ✅ (9/9)`
- **有违规**: `编码规范审计 ❌ (N/9)` + 逐条违规明细（文件:行号 [规则] 描述）
- **退出码**: 0 = 全部通过，1 = 有违规

## 工作流集成

1. 完成代码修改后，对修改的文件运行审计
2. 如有违规，**先修复**再继续
3. 全部通过后，在总结中追加 `编码规范审计 ✅ (9/9)`

## 智能排除

脚本自动排除以下情况，避免误报：
- `_test.go` 测试文件
- `vendor/` 目录
- `New...` 构造函数的 context 检查（构造阶段通常不执行 I/O）
- `*gin.Context` 参数的 Gin handler（通过 `c.Request.Context()` 间接获取）
- 返回 `*gorm.DB` 的 scope/builder 函数
- Gin 中间件的外层闭包（嵌套阈值放宽为 3 层）
