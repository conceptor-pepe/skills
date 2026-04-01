---
inclusion: manual
---

# PRD to Plan（PRD 转实施计划）

适用于：用户说「PRD 转计划」「拆分 PRD」「垂直切片」「分阶段计划」，或已有 PRD 准备开始规划实施时。

## 前提条件

PRD 必须已在对话上下文中，或存放于 `docs/features/<feature-name>/prd.md`。如果没有，先使用 `write-a-prd` steering。

## 流程

### 第 1 步：确认 PRD

确认 PRD 已加载到上下文。

### 第 2 步：探索代码库

理解当前架构，重点关注：

- 现有路由结构和注册方式（`internal/*/handlers.go`）
- 数据库 Schema（`database_schema.md`）
- Wire 依赖注入（`internal/*/wire.go`）
- 相似功能模块的实现方式

### 第 3 步：识别持久架构决策

在切片之前，先确定不会随实施变化的架构基础：

- 路由路径和分组
- 数据库 Schema 形状（表名、关键字段）
- 鉴权策略
- 关键数据模型名称

### 第 4 步：拆解垂直切片

将 PRD 拆解为 **tracer bullet phases**。每个 Phase 必须：

- 穿透所有层：Schema → Repository → Service → Handler → 测试
- 独立可演示或可验证
- 宁可切片更细，不要过厚

**反例（水平切片，禁止）：**
- Phase 1：建所有数据库表
- Phase 2：写所有 Service 逻辑

**正例（垂直切片）：**
- Phase 1：用户可以查询自己的资产列表（含分页）
- Phase 2：用户可以上传新资产（含文件存储）

### 第 5 步：与用户确认

以编号列表呈现每个 Phase，询问粒度是否合适，迭代直到用户确认。

### 第 6 步：写计划文件

写入 `docs/features/<feature-name>/task_plan.md`。

---

## 计划文件模板

```markdown
# 实施计划：<功能名称>

> 来源 PRD：docs/features/<feature-name>/prd.md
> 创建日期：YYYY-MM-DD

## 架构决策

适用于所有 Phase 的持久决策：

- **路由**：...
- **Schema**：...
- **鉴权**：...

---

## Phase 1：<标题>

**覆盖用户故事**：#1, #3

### 要构建的内容

描述这个垂直切片的端到端行为。

### 验收标准

- [ ] 标准 1
- [ ] 标准 2
```

---

## 注意事项

- 垂直切片的核心原则：每个切片必须"可演示"，而非"某一层完成了"
- 计划文档不写具体文件路径和函数名，只写行为和验收标准
- 用中文输出所有内容
