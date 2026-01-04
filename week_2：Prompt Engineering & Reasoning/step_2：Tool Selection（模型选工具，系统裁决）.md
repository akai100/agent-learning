**目标一句话：**

👉 让模型“提出想用的工具”，但是否真的执行由系统决定

这是 **Agent 工程里最重要的分权设计。**

**一、你现在的 Agent 还缺什么？**

你目前的 Agent 是：

+ ✅ 有 FSM

+ ✅ 有 Tool Router

+ **❌ 工具是“被动调用”的**

+ ❌ 模型只是“照 Prompt 写 Action”

真实世界需要的是：

+ 模型 = 决策建议者

+ 系统 = 最终执行者

**二、Tool Selection 的正确分层**

我们把“用工具”拆成 3 层：

```sql
1️⃣ Model Proposal（模型建议）
2️⃣ System Validation（系统校验）
3️⃣ Tool Execution（真实执行）
```

❗ 永远不要让模型直接“执行”

**三、设计升级（不推翻现有架构）**

我们只做 两件事：

1. 把 Action 升级成 “候选动作”

2. 引入 Tool Selector / Validator
