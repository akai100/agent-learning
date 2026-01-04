目标一句话：

👉 任务完成后，Agent 不只是结束，

👉 而是 总结经验 → 提炼规律 → 反哺下一次执行

这是 Agent 从
“能完成任务” → “下次做得更好” 的关键。

## 一、为什么必须做 Execution Review？

目前为止，你已经有：

+ Planning / Re-planning

+ Plan-aware Memory

+ Tool Affinity Learning

但少了一步：

**把“发生过的事”变成“可复用的经验”**

否则：

+ 学习是隐式的、不可解释的

+ 人无法理解 Agent 为什么变“聪明”

+ 无法人工干预或调参

## 二、Execution Review 的工程定位

⚠️ 非常重要：

Review ≠ 再执行一次任务
Review = 离线反思（Offline Reasoning）

它发生在：

```
Agent DONE 之后
```

## 三、Review 的输入与输出（先想清楚）

输入（系统提供）

+ 原始 Task

+ Final Plan（含 version）

+ 每个 Step 的：

  + 成功 / 失败

  + 使用的工具

  + 重试次数

+ Tool Affinity 当前状态

输出（结构化）

1. 哪些 Step 做得好

2. 哪些 Step 有问题（原因）

3. 工具选择是否合理

4. 下次执行的改进建议

## 四、Review 数据结构（关键）

```review.py```

```python
from dataclasses import dataclass
from typing import List

@dataclass
class StepReview:
    step_id: int
    description: str
    success: bool
    notes: str

@dataclass
class ExecutionReview:
    task: str
    plan_version: int
    step_reviews: List[StepReview]
    overall_summary: str
    improvement_suggestions: List[str]
```

## 五、Review Generator（模型只负责“反思”）

```reviewer.py```

```python
class ExecutionReviewer:
    def __init__(self, llm):
        self.llm = llm

    def review(self, task, plan, memory) -> ExecutionReview:
        prompt = f"""
You are reviewing an agent execution.

Task:
{task}

Plan (version {plan.version}):
"""        

        for step in plan.steps:
            step_mem = memory.steps.get(step.id)
            prompt += f"\nStep [{step.id}] {step.description}\n"
            if step_mem:
                prompt += f"- Actions: {step_mem.actions}\n"
                prompt += f"- Errors: {step_mem.errors}\n"
            else:
                prompt += "- No data\n"

        prompt += """
Provide:
1. Step-by-step evaluation (success/failure + reason)
2. Overall execution summary
3. Concrete improvement suggestions for future runs

Respond in clear bullet points.
"""

        output = self.llm.call([
            {"role": "system", "content": prompt}
        ])

        # 教学版：这里不做复杂解析，直接存文本
        return ExecutionReview(
            task=task,
            plan_version=plan.version,
            step_reviews=[],
            overall_summary=output,
            improvement_suggestions=[]
        )
```

👉 关键点

+ Review 不调用工具

+ Review 不影响当前执行

+ Review 是“事后智能”

## 六、把 Review 接入 Agent（非常简单）

```agent.py``` 在 DONE 时加入：

```python
from reviewer import ExecutionReviewer
```


在 ```__init__```：

```python
self.reviewer = ExecutionReviewer(self.llm)
```


在完成任务后：

```python
print("\n🧾 Execution Review:")
review = self.reviewer.review(
    task,
    self.plan,
    self.memory
)
print(review.overall_summary)
```

## 七、如何“真正用上” Review（工程关键）

**方式 1️⃣ 人工查看（最常见）**

+ 用于调 Prompt / Rule / Tool

**方式 2️⃣ 半自动**

+ 人工把 Review 中的建议转为：

  + 新 Router 规则
  
  + 新 Tool Affinity 初始化值

**方式 3️⃣ 全自动（高级）**

+ 提取 Review 中的：

  + “calculator 在 math 步骤成功率高”

+ 自动写入 Affinity Store

⚠️ 真正生产系统通常 2️⃣ + 3️⃣ 混合

## 八、你现在拥有的 Agent 能力全景

到 第 3 周结束，你已经完整实现了：

🧠 思考

+ ReAct

+ Planning

+ Re-planning

🧭 决策

+ Tool Proposal

+ Ranking

+ Tool Affinity Learning

🧠 记忆

+ Plan-aware Memory

+ Execution Logs

**🔁 稳定性**

+ Retry

+ Error Recovery

📈 进化

Execution Review

Self-Critique

这是 真正意义上的 Agent 系统
