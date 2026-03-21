# 测试功能 Review

## 触发时机
在 Code Review 完成后，或完成一阶段功能实现后执行。

## 工作流程

### 第一步：理解被 Review 的代码
分析刚刚 review 过的代码，识别：
- 核心业务逻辑和关键路径
- 对外暴露的函数/方法
- 涉及的数据流转

### 第二步：设计测试用例（伪代码/描述形式）

针对每个核心函数，从以下维度设计测试用例：

**正常路径（Happy Path）**
- 典型输入 → 预期输出
- 边界值（最小值、最大值、空集合）

**异常路径（Error Path）**
- 无效输入（nil、空字符串、负数、零值）
- 依赖失败（DB 错误、Redis 超时、外部服务不可用）
- 并发场景（竞态条件、重复请求）

**边界条件（Edge Cases）**
- 空列表/空结构体
- 超大数据量
- 特殊字符/编码问题

### 第三步：逐条对照代码评审

对每个测试用例，检查代码是否正确处理：

```
测试用例: [描述]
预期行为: [期望结果]
代码现状: ✅ 已处理 / ⚠️ 部分处理 / ❌ 未处理
问题说明: [如有问题，说明原因]
```

### 第四步：输出结论

**必须修复（影响正确性）**
- 列出 ❌ 未处理的用例及修复建议

**建议优化（提升健壮性）**
- 列出 ⚠️ 部分处理的用例及改进方向

**测试覆盖建议**
- 建议补充的单元测试用例（Go testify 格式）

## Go 项目测试规范

测试用例遵循项目规范：
- 使用 `testify/assert` 断言
- 表驱动测试 `t.Run(name, func(t *testing.T){})`
- Mock 依赖使用接口
- 测试文件命名：`xxx_test.go`

示例结构：
```go
func TestXxx(t *testing.T) {
    tests := []struct {
        name    string
        input   InputType
        want    OutputType
        wantErr bool
    }{
        {name: "正常情况", input: ..., want: ..., wantErr: false},
        {name: "空输入", input: ..., wantErr: true},
        {name: "DB错误", input: ..., wantErr: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // arrange
            // act
            // assert
        })
    }
}
```
