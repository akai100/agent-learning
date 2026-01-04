目标一句话：

👉 让 Agent 的 Memory**绑定到 Plan & Step，**

👉 不再是「做过什么」，而是「在第几步，用什么方法，结果如何」

**一、为什么普通 Memory 不够？**

你现在的短期 Memory 只能回答：

+ 做过哪些 action？

+ 最近发生了什么错误？

但 不能回答：

+ ❓ 哪一步最容易失败？

+ ❓ 在第 3 步用 calculator 好还是 search 好？

+ ❓ 当前失败是“策略错”还是“执行错”？

👉 因为 Memory 没有 Plan 维度

**二、核心设计**

我们把 Memory 从：

```
time-based log
```

升级为

```
PlanStep-aware structured memory
```

**三、Memory 结构升级**

```memory.py``` **（新增 Plan 维度）**

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class StepMemory:
    actions: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PlanAwareMemory:
    steps: Dict[int, StepMemory] = field(default_factory=dict)
    rejected_actions: List[str] = field(default_factory=list)

    def _get_step(self, step_id: int) -> StepMemory:
        if step_id not in self.steps:
            self.steps[step_id] = StepMemory()
        return self.steps[step_id]

    def record_action(self, step_id, tool, input):
        self._get_step(step_id).actions.append({
            "tool": tool,
            "input": input
        })

    def record_observation(self, step_id, obs):
        self._get_step(step_id).observations.append(obs)

    def record_error(self, step_id, error):
        self._get_step(step_id).errors.append(error)

    def record_rejection(self, reason):
        self.rejected_actions.append(reason)

    def summary(self, step_id: int) -> str:
        """
        只返回当前 Plan Step 相关记忆
        """
        step = self.steps.get(step_id)
        if not step:
            return ""

        parts = []

        if step.actions:
            parts.append(
                "Previous actions in this step: " +
                ", ".join(
                    f"{a['tool']}({a['input']})"
                    for a in step.actions[-2:]
                )
            )

        if step.errors:
            parts.append(
                "Errors in this step: " +
                "; ".join(step.errors[-1:])
            )

        return "\n".join(parts)
```

👉 关键点

+ Memory 按 Step 隔离

+ 不污染其它步骤

+ 失败不“传染”

**四、Agent 接入 Plan-aware Memory**

```agent.py``` **替换原 Memory**

```python
agent.py 替换原 Memory
```

在 __init__：

```python
self.memory = PlanAwareMemory()
```

**在主循环中获取当前 Step**

你已经有：

```python
current_step = self.plan.next_step()
```

我们在后续全部传入 ```current_step.id```

**记录 Memory（关键变化）**

**工具执行成功**

```python
self.memory.record_action(
    current_step.id,
    candidate.tool,
    candidate.input
)

self.memory.record_observation(
    current_step.id,
    observation
)
```

**工具执行成功：**

```python
self.memory.record_action(
    current_step.id,
    candidate.tool,
    candidate.input
)

self.memory.record_observation(
    current_step.id,
    observation
)
```

**出错时：**

```python
self.memory.record_error(
    current_step.id,
    str(e)
)
```

**被拒绝时：**

```python
self.memory.record_rejection(reason)
```

**注入 Memory Summary（只注入当前 Step）**

```python
step_memory = self.memory.summary(current_step.id)
if step_memory:
    self.messages.append({
        "role": "system",
        "content": f"Memory for current plan step:\n{step_memory}"
    })
```
👉 这是关键中的关键

模型只看到「当前这一步的历史」

**五、Prompt 微调（让模型“意识到 Step”）**

在 SYSTEM_PROMPT 末尾补一句：

```python
You are executing a multi-step plan.
Use ONLY memory related to the current plan step.
Do not repeat actions that failed in this step.
```
