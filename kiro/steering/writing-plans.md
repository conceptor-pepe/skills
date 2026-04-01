---
inclusion: always
---

# 任务拆分与实现计划（Writing Plans）

## 触发时机

需求/方案确认后（brainstorming 完成），开始实现前，必须先拆分任务计划。

---

## 拆分原则

### 粒度标准：每个任务 5-15 分钟
- 一个任务只做一件事：新增一个函数、修改一个接口、写一组测试
- 任务之间尽量独立，可单独验证
- 不要把"实现整个 service"作为一个任务

### 每个任务必须包含

```
### Task N: <任务名>

**涉及文件：**
- 新增：`internal/xxx/yyy.go`
- 修改：`internal/xxx/zzz.go`

**实现要点：**
- 具体要做什么（不是"添加逻辑"，而是"在 CreateOrder 中调用 deductCredit"）

**验证方式：**
- go build ./...          # 编译通过
- go test ./internal/xxx/...  # 相关测试通过
- （如有）curl 示例或手动验证步骤
```

---

## 任务顺序原则

按依赖关系从底层到上层排列：

1. model / constants（数据结构）
2. repository（数据访问）
3. service（业务逻辑）
4. handler / DTO（接口层）
5. 路由注册 / wire（模块接入）
6. 测试补充

### 跨层依赖处理

当多层需要同时新增（如 model + service 强耦合）时，优先拆出**最小可编译单元**：

- 先只定义 struct 和 interface，不写实现 → 编译通过
- 再逐层填充实现
- 原则：每个 task 完成后必须能 `go build ./...` 通过，不允许出现半成品导致编译失败的中间状态

---

## 计划文档保存

保存到 `.kiro/specs/<feature-name>/tasks.md`，使用表格格式便于追踪：

```markdown
| # | 任务 | 涉及文件 | 验证方式 |
|---|------|----------|----------|
| 1 | 新增 Order model | 新增 `internal/order/model/order.go` | `go build ./...` |
| 2 | 实现 OrderRepository.Create | 修改 `internal/order/repository/order.go` | `go build ./...` |
| 3 | 实现 OrderService.CreateOrder | 修改 `internal/order/service/order.go` | `go test ./internal/order/...` |
| 4 | 实现 POST /orders handler | 修改 `internal/order/handler/order.go` | `go build ./...` |
| 5 | 注册路由和 wire | 修改 `internal/order/handlers.go`, `wire.go` | `go build ./...` |
```

---

## 反模式

- 任务粒度太大：「实现订单模块」→ 无法验证、无法追踪
- 缺少验证步骤：不知道任务是否完成
- 顺序混乱：上层依赖下层，必须先实现底层
- 跳过计划直接写代码 → 容易遗漏、难以 review
