**目标一句话：**

👉 让 Agent **把 Execution Review / 成功经验 / 失败教训**

👉 变成 **可检索、可复用的长期知识**

## 一、先把概念彻底讲清楚

**三种 Memory 的分工**

| 类型                    | 生命周期    | 用途        |
| --------------------- | ------- | --------- |
| **短期 Memory**         | 单次运行    | 防重复、稳定执行  |
| **Plan-aware Memory** | 单次 Plan | 步骤级理性     |
| **长期 Memory**         | 跨任务     | 经验复用、迁移学习 |

⚠️ 长期 Memory ≠ 聊天记录

## 二、长期 Memory 应该存什么？

✅ 应该存

+ 成功的 Plan 模式

+ 某类任务 → 某类工具效果好

+ 失败原因总结（抽象层）

❌ 不该存

+ 原始对话全文

+ 临时 Observation

+ 噪声日志

## 三、长期 Memory 的最小可用形态（不直接上向量库）

我们先做一个 **结构化 + 可检索** 的版本：

```css
experience_id
task_type
summary
tags
embedding（后面加）
```

## 四、定义 Experience 数据结构

```long_term_memory.py```

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Experience:
    id: str
    task_type: str
    summary: str
    tags: List[str]
```

## 五、Experience Store （可持久化）

```experience_store.py```

```python
import json
import uuid

class ExperienceStore:
    def __init__(self, path="experiences.json"):
        self.path = path
        self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, task_type, summary, tags):
        exp = {
            "id": str(uuid.uuid4()),
            "task_type": task_type,
            "summary": summary,
            "tags": tags
        }
        self.data.append(exp)
        self._save()

    def search_by_tag(self, tag):
        return [
            e for e in self.data
            if tag in e["tags"]
        ]
```
