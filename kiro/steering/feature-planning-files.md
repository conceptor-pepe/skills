---
inclusion: always
---

# 特性文档归档规范（强制）

## 规则

每个特性的所有文档（PRD、计划、调研、进度等）**必须**放在 `docs/features/<feature-name>/` 下，**禁止**散落在项目根目录或其他位置。

## 目录结构

```
docs/features/<feature-name>/
├── prd.md                      # PRD 需求文档
├── task_plan.md                # 实施计划（Phase 拆分）
├── findings.md                 # 调研发现
├── progress.md                 # 进度记录
└── (其他相关文档)
```

## `<feature-name>` 命名

- 使用 kebab-case（如 `admin-auth`、`canvas-export`、`payment-refund`）
- 简洁表达特性主题，1-3 个单词

## 执行流程

1. 新特性启动时，先 `mkdir -p docs/features/<feature-name>/`
2. PRD 命名为 `prd.md`，直接放在该目录
3. 规划文件（task_plan / findings / progress）同样放在该目录
4. 后续该特性相关的设计文档、迁移说明等也放在同一目录

## 禁止

- **禁止** `task_plan.md`、`findings.md`、`progress.md` 出现在项目根目录
- **禁止** 特性文档散落在不同目录
- **禁止** 不同特性的文档混在同一个目录
