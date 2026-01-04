目标一句话：

👉 当某个 Plan Step 反复失败或不再可行时，

👉 Agent 不是硬撑，而是修改计划

这是 “**执行系统**” vs “**智能系统**” 的分水岭。

**一、什么情况下必须 Re-plan？**

不是每次失败都要重规划。

我们定义**3 类触发条件：**

**🔴 必须 Re-plan**

1. 同一步 连续失败 ≥ N 次

2. 所需工具 被禁用 / 不存在

3. 当前 Step 的前置假设被推翻

**🟡 建议 Re-plan**

4. 成本超预算

5. 时间超阈值

**🟢 不需要**

6. 偶发工具错误（可 retry）

**二、核心原则（一定要记住）**

Re-plan 不是从 0 开始

👉 而是 在当前执行上下文下修补计划

**三、工程设计（最小但完整）**

我们引入 3 个新能力：

```
PlanEvaluator   # 判断是否需要 Re-plan
RePlanner       # 修改计划
Plan Versioning # 计划版本管理
```

**四、Plan 版本化（非常关键）**

```plan.py``` **升级**

```python
@dataclass
class Plan:
    goal: str
    steps: List[PlanStep]
    version: int = 1

    def next_step(self):
        for step in self.steps:
            if not step.done:
                return step
        return None

    def failed_count(self, step_id: int, memory) -> int:
        step_mem = memory.steps.get(step_id)
        if not step_mem:
            return 0
        return len(step_mem.errors)
```

**五、PlanEvaluator：什么时候该重规划**

```plan_evaluator.py```

```python
class PlanEvaluator:
    def __init__(self, max_failures=2):
        self.max_failures = max_failures

    def should_replan(self, plan, current_step, memory) -> bool:
        failures = plan.failed_count(current_step.id, memory)
        if failures >= self.max_failures:
            return True
        return False
```

**六、RePlanner：只修改“失败那一段”**

```replanner.py```

```python
from planner import Planner
from plan import PlanStep

class RePlanner:
    def __init__(self, llm):
        self.llm = llm
        self.planner = Planner(llm)

    def replan(self, plan, failed_step):
        prompt = f"""
The following plan step failed repeatedly:

Step [{failed_step.id}]: {failed_step.description}

Revise the plan starting from this step.
Do NOT redo completed steps.
Provide a revised sequence starting at this step.

Format:
1. <new step>
2. <new step>
...
"""

        output = self.llm.call([
            {"role": "system", "content": prompt}
        ])

        new_steps = []
        for i, line in enumerate(output.splitlines(), start=failed_step.id):
            line = line.strip()
            if line and line[0].isdigit():
                desc = line.split(".", 1)[1].strip()
                new_steps.append(PlanStep(i, desc))

        if not new_steps:
            raise ValueError("Re-planning failed")

        # 替换失败 step 及之后的步骤
        plan.steps = (
            plan.steps[:failed_step.id - 1] + new_steps
        )
        plan.version += 1

        return plan
```

👉 关键点

+ 已完成的步骤不动

+ 只修失败区段

+ Plan 有版本号

**七、Agent 接入 Re-planning**

**在**```agent.py``` **初始化：**

```python
from plan_evaluator import PlanEvaluator
from replanner import RePlanner

self.plan_evaluator = PlanEvaluator(max_failures=2)
self.replanner = RePlanner(self.llm)
```

**在执行某一步失败后，加入判断：**

```python
if self.plan_evaluator.should_replan(
    self.plan,
    current_step,
    self.memory
):
    print("🧠 Triggering dynamic re-planning...")
    self.plan = self.replanner.replan(
        self.plan,
        current_step
    )
    continue
```

👉 注意：

+ 发生在 retry 之前或之后都可以

+ 但一定要 在继续执行前
