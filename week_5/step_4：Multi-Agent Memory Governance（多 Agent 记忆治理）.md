**一句话目标：**

👉 不是每个 Agent 都有“记忆写权限”

👉 Memory 是 **系统资产，不是 Agent 私有财产**

这是防止 **经验污染、幻觉固化** 的核心设计。

## 一、如果不做 Memory Governance，会发生什么？

真实会遇到的问题：

+ ❌ Executor 把错误 Observation 写成经验

+ ❌ Critic 把“猜测”写成事实

+ ❌ Planner 把失败计划当最佳实践

👉 结果：

**Memory 迅速变成垃圾场**

## 二、Memory Governance 的三条铁律

**铁律 1**

读权限 > 写权限

**铁律 2**

写 Memory 必须经过“系统层”

**铁律 3**

所有 Memory 可追责（Audit）

## 三、定义 Memory 权限模型

| Agent    | Read | Propose | Write | Delete |
| -------- | ---- | ------- | ----- | ------ |
| Planner  | ✅    | ❌       | ❌     | ❌      |
| Executor | ✅    | ❌       | ❌     | ❌      |
| Critic   | ✅    | ✅       | ❌     | ❌      |
| Manager  | ✅    | ✅       | ✅     | ✅      |

👉 只有 Manager 能真正写入 / 删除 Memory


## 四、Memory Proposal（关键中间层）

我们引入一个新概念：

  MemoryProposal = “建议写入”，不是“直接写入”

```memory_proposal.py```


