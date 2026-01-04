目标一句话：

👉 让 Agent**先生成一个可执行计划（Plan），**

👉 再由系统**逐步、可控地执行**

**一、为什么一定要加 Planning？**

你现在的 Agent 已经很强，但它仍然：

+ 容易「走一步算一步」

+ 长任务中途跑偏

+ 无法提前发现不可能完成的任务

现实系统里：

+ 执行 ≠ 决策

+ 规划 ≠ 行动

**二、Agent 架构升级（非常关键）**

我们把 Agent 拆成三层：

```
Planner  ->  Executor  ->  Tools
```

+ Planner：负责想清楚要干什么

+ Executor：负责一步步做

+ Tools：无脑执行

你已经有：

+ Executor（Agent Loop）

+ Tools

现在只缺 Planner

**三、Plan 的工程定义**

一个**可执行 Plan**必须满足：

1. 步骤是有序的

2. 每步是原子任务

3. 可以映射到工具或子问题

4. 允许失败 & 回滚

**四、我们先做「最小可用 Plan」（MVP）**

设计一个结构化 Plan

```python
from dataclasses import dataclass
from typing import List

@dataclass
class PlanStep:
    id: int
    description: str
    done: bool = False


@dataclass
class Plan:
    goal: str
    steps: List[PlanStep]

    def next_step(self):
        for step in self.steps:
            if not step.done:
                return step
        return None

    def mark_done(self, step_id: int):
        for step in self.steps:
            if step.id == step_id:
                step.done = True
                return

```

**五、Planner：让模型只做一件事「拆任务」**

```python
import re
from plan import Plan, PlanStep

class Planner:
    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, task: str) -> Plan:
        prompt = f"""
You are a planner.

Decompose the task into clear, ordered steps.
Each step should be minimal and executable.

Format:
1. <step description>
2. <step description>
...

Task:
{task}
"""
        output = self.llm.call([
            {"role": "system", "content": prompt}
        ])

        steps = []
        for i, line in enumerate(output.splitlines(), start=1):
            line = line.strip()
            if re.match(r"\d+\.", line):
                desc = line.split(".", 1)[1].strip()
                steps.append(PlanStep(i, desc))

        if not steps:
            raise ValueError("Failed to create plan")

        return Plan(goal=task, steps=steps)
```

👉 关键点：

+ Planner 不调用工具

+ Planner 不执行

+ Planner 只输出 Plan

**六、把 Planning 接入 Agent**

agent.py 新增字段

```python
from planner import Planner
```

在```__init__```：

```python
self.planner = Planner(llm)
self.plan = None
```

在 ```run()``` 一开始生成 Plan

```python
print("\n🧭 Creating execution plan...")
self.plan = self.planner.create_plan(task)

for step in self.plan.steps:
    print(f"  - [{step.id}] {step.description}")
```

**每一轮只执行一个 PlanStep**

在主循环里，**替换原来的 user task：**

```python
current_step = self.plan.next_step()

if current_step is None:
    print("\n✅ All plan steps completed")
    self.state = AgentState.DONE
    return

step_prompt = (
    f"Current plan step:\n"
    f"[{current_step.id}] {current_step.description}\n"
    "Focus ONLY on completing this step."
)

self.messages.append({
    "role": "user",
    "content": step_prompt
})
```

**Step 完成后标记 Done**

当 Agent 选择 NONE（完成）：

```python
self.plan.mark_done(current_step.id)
```
