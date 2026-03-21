---
name: prd-to-plan
description: 将 PRD 拆解为垂直切片（tracer bullet）分阶段实施计划，保存到 docs/plans/，并衔接 writing-plans 或 executing-plans。适用于：用户说「PRD 转计划」「拆分 PRD」「垂直切片」「分阶段计划」，或已有 PRD 准备开始规划实施时。
---

# PRD to Plan（PRD 转实施计划）

**开场白：** 我正在使用 prd-to-plan skill 将 PRD 拆解为垂直切片计划。

## 前提条件

PRD 必须已在对话上下文中，或存放于 `docs/prds/`。如果没有，先使用 `write-a-prd` skill。

## 流程

### 第 1 步：确认 PRD

确认 PRD 已加载到上下文。如果用户提供的是文件路径，读取该文件。

### 第 2 步：探索代码库

理解当前架构、现有模式和集成层，重点关注：

- 现有路由结构和注册方式（`internal/*/handlers.go`）
- 数据库 Schema（`database_schema.md`）
- Wire 依赖注入（`internal/wire/`）
- 相似功能模块的实现方式

### 第 3 步：识别持久架构决策

在切片之前，先确定不会随实施变化的架构基础：

- 路由路径和分组
- 数据库 Schema 形状（表名、关键字段）
- 鉴权策略（是否需要 JWT 中间件）
- 关键数据模型名称
- 第三方服务边界

这些内容会写入计划文档头部，供每个 Phase 引用。

### 第 4 步：拆解垂直切片

将 PRD 拆解为 **tracer bullet phases**。每个 Phase 必须：

- 穿透所有层：Schema → Repository → Service → Handler → 测试
- 独立可演示或可验证
- 宁可切片更细，不要过厚
- 不包含容易变动的实现细节（函数名、文件路径）
- 包含持久决策（路由路径、Schema 字段、模型名称）

**反例（水平切片，禁止）：**
- Phase 1：建所有数据库表
- Phase 2：写所有 Service 逻辑
- Phase 3：写所有 Handler

**正例（垂直切片）：**
- Phase 1：用户可以查询自己的资产列表（含分页）
- Phase 2：用户可以上传新资产（含文件存储）
- Phase 3：用户可以编辑资产元数据

### 第 5 步：与用户确认

以编号列表呈现每个 Phase，每条包含：

- **标题**：简短描述
- **覆盖的用户故事**：对应 PRD 中的编号

询问用户：
- 粒度是否合适？（太粗 / 太细）
- 是否需要合并或拆分某些 Phase？

迭代直到用户确认。

### 第 6 步：写计划文件

创建 `docs/plans/`（如不存在），写入 `docs/plans/YYYY-MM-DD-<feature>.md`。

---

## 计划文件模板

```markdown
# 实施计划：<功能名称>

> 来源 PRD：docs/prds/YYYY-MM-DD-<feature>.md
> 创建日期：YYYY-MM-DD

## 架构决策

适用于所有 Phase 的持久决策：

- **路由**：...
- **Schema**：...
- **鉴权**：...
- **关键模型**：...

---

## Phase 1：<标题>

**覆盖用户故事**：#1, #3

### 要构建的内容

描述这个垂直切片的端到端行为，而非逐层实现。

### 验收标准

- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

---

## Phase 2：<标题>

**覆盖用户故事**：#5, #7

### 要构建的内容

...

### 验收标准

- [ ] ...
```

---

## 衔接下一步

计划保存后，提示用户：

> 计划已保存至 `docs/plans/YYYY-MM-DD-<feature>.md`。
>
> 执行方式：
> 1. **子代理驱动（当前会话）** → 使用 `writing-plans` + `executing-plans`，每个 Phase 分别执行并 review
> 2. **新会话并行执行** → 在新会话中打开计划文件，使用 `executing-plans` 按 Phase 批量执行

## 注意事项

- 垂直切片的核心原则：每个切片必须"可演示"，而非"某一层完成了"
- 计划文档不写具体文件路径和函数名，只写行为和验收标准
- 切片之间尽量无依赖，或依赖关系明确（后置 Phase 依赖前置 Phase）
- 用中文输出所有内容
