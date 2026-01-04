目标一句话：

👉 Agent 不再“每次都重新猜用什么工具”，

👉 而是 在不同 Plan Step 类型下，学会偏好最有效的工具

这是 Agent 从 “会做事” → “会选路” 的跃迁。

**一、为什么必须做 Tool Affinity？**

你现在的 Agent 已经能：

+ 多工具候选

+ Ranking

+ Planning & Re-planning

但它仍然：

+ 每一步都像第一次选工具

+ 对“哪种任务用哪种工具”没有长期记忆

+ Ranking 规则靠人写，越写越复杂

**👉 Tool Affinity = 可学习的 Ranking Bias**

**二、核心思想**

不让模型“记经验”

让系统统计“工具在某类步骤中的效果”

我们学习的是：

```
(step_type, tool) -> success score
```

而不是自然语言

**三、定义 Step Type（关键抽象）**

我们先给每个 Plan Step 一个**类型标签：**

**示例 Step Types**

+ math

+ lookup

+ reasoning

+ writing

+ verification

**1️⃣ 给 PlanStep 增加 type**

```plan.py```

```python
@dataclass
class PlanStep:
    id: int
    description: str
    step_type: str = "general"   # 新增 type
    done: bool = False
```

**2️⃣ Planner 生成 Step Type（轻 Prompt）**

```planner.py```  **（create_plan prompt 改造）**

```python
prompt = f"""
Decompose the task into ordered steps.

For each step, assign a type from:
- math
- lookup
- reasoning
- writing
- verification

Format:
1. [type] step description
2. [type] step description
...

Task:
{task}
"""
```

**解析：**

```python
if re.match(r"\d+\.\s*\[", line):
    type_part = line.split("[", 1)[1].split("]", 1)[0]
    desc = line.split("]", 1)[1].strip()
    steps.append(
        PlanStep(i, desc, step_type=type_part)
    )
```

**👉 Step Type 是工具学习的锚点**

```四、Tool Affinity Store（学习核心）```

```tool_affinity.py```

```python
from collections import defaultdict

class ToolAffinityStore:
    def __init__(self):
        # (step_type, tool) -> score
        self.scores = defaultdict(int)

    def record_success(self, step_type, tool):
        self.scores[(step_type, tool)] += 1

    def record_failure(self, step_type, tool):
        self.scores[(step_type, tool)] -= 1

    def affinity(self, step_type, tool):
        return self.scores.get((step_type, tool), 0)
```

👉 简单、可解释、可持久化

**五、把 Affinity 接入 Tool Selector（关键）**

```selector.py``` 升级

**初始化：**

```python
class ToolSelector:
    def __init__(self, router, affinity_store):
        self.router = router
        self.affinity = affinity_store
```

**在 score() 中加入 Affinity Bias：*

```python
def score(self, state, candidate, step_type):
    if candidate.is_done:
        return 100

    if not self.router.is_allowed(state, candidate.tool):
        return -100

    score = 0

    # 基础规则
    if candidate.tool == "calculator":
        score += 10
    if candidate.tool == "search_stub":
        score += 5

    # 🔥 Tool Affinity Bias
    score += self.affinity.affinity(
        step_type,
        candidate.tool
    )

    return score
```

**六、在 Agent 中“学习”**

**成功执行后：**

```python3
self.affinity_store.record_success(
    current_step.step_type,
    candidate.tool
)
```

**失败或被拒绝后：**

```python
self.affinity_store.record_failure(
    current_step.step_type,
    candidate.tool
)
```

👉 这就是 系统级强化信号

## 七、现在 Agent 的行为发生了什么变化？

初期

+ 每一步都靠规则

+ 成功率一般

**运行一段时间后**

+ 数学步骤自动偏 calculator

+ lookup 步骤更倾向 search

+ 某些工具在某些 step_type 下被“淘汰”

**👉 Agent 开始形成“使用习惯”**


## 八、非常重要的设计原则（一定记住）

❌ 不要

+ 把 Affinity 直接塞进 Prompt

+ 让模型“记得哪个工具好”

✅ 要

+ 系统统计

+ 系统偏置

+ 模型只负责提方案

**模型负责可能性，系统负责偏好**
