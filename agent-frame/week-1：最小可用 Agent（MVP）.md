## 一、这个 Agent 能做什么？

+ ✅ 使用 ReAct Prompt

+ ✅ 支持 工具调用

+ ✅ 有 Agent Loop

+ ❌ 不追求优雅、不追求完备

+ ❌ 不用 LangChain / AutoGen

## 二、项目结构（极简）

```
week1_min_agent/
├── agent.py          # Agent 主循环
├── tools.py          # 工具定义
├── prompt.py         # System Prompt
└── run.py            # 启动入口
```

## 三、System Prompt（Agent 的“宪法”）

```prompt.py```

```python3
SYSTEM_PROMPT = """
You are a ReAct-style AI Agent.

You must strictly follow this format in every response:

Thought: describe what you are thinking
Action: the tool name and input (or NONE)
Observation: result of the action (leave empty if no action)

Rules:
1. If you do not need a tool, set Action to NONE.
2. Do not make up observations.
3. Think step by step.
4. Stop when you reach a final answer.

Available tools:
- calculator: evaluate a math expression
"""
```

**⚠️ 关键点**

+ 强制输出结构

+ 明确工具列表

+ 明确“不允许编造 Observation”

## 四、工具定义（Agent 的“手”）

```tools.py```

```python3
def calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


TOOLS = {
    "calculator": calculator
}
```

现在工具很原始，但这是**Agent 调用真实世界的起点**

## 五、Agent 核心（灵魂代码）

```agent.py```

```python3
import re
from prompt import SYSTEM_PROMPT
from tools import TOOLS

class ReActAgent:
    def __init__(self, llm_call):
        self.llm_call = llm_call
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def parse_action(self, text: str):
        """
        从模型输出中解析 Action
        """
        match = re.search(r"Action:\s*(.*)", text)
        if not match:
            return None, None

        action = match.group(1).strip()
        if action == "NONE":
            return "NONE", None

        # 例：calculator: 2 + 3
        if ":" in action:
            tool, arg = action.split(":", 1)
            return tool.strip(), arg.strip()

        return None, None

    def step(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        response = self.llm_call(self.messages)

        self.messages.append({"role": "assistant", "content": response})
        print("\nAgent Output:\n", response)

        tool_name, tool_input = self.parse_action(response)

        if tool_name == "NONE":
            return False  # 结束

        if tool_name in TOOLS:
            observation = TOOLS[tool_name](tool_input)
        else:
            observation = f"Unknown tool: {tool_name}"

        # 把 Observation 喂回模型
        obs_text = f"Observation: {observation}"
        self.messages.append({"role": "user", "content": obs_text})
        print("\nObservation:\n", observation)

        return True  # 继续
```

## 六、LLM 调用 & 启动入口

```run.py```

```python3
from agent import ReActAgent
import openai

openai.api_key = "YOUR_API_KEY"

def llm_call(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # 或你能用的模型
        messages=messages,
        temperature=0
    )
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    agent = ReActAgent(llm_call)

    task = "What is (12 * 7) + 5?"
    running = True

    while running:
        running = agent.step(task)
        task = ""  # 后续轮次不再重复问题
```

## 七、你第一次跑通时应该看到什么？

类似这样：

```
Thought: I need to calculate (12 * 7) + 5.
Action: calculator: 12 * 7 + 5
Observation: 89
Thought: I have the result.
Action: NONE
```

🎉 **恭喜，这是一个真正的 Agent**

## 八、第 1 周你必须“亲手改”的 5 个点（非常重要）

不要直接进第 2 周，先完成这些：

1. ❗ 把 calculator 改坏一次，看看 Agent 如何崩

2. ❗ 让模型输出不符合格式，观察系统怎么死

3. ❗ 改 temperature，观察行为变化

4. ❗ 加一个新工具（比如 search_stub）

5. ❗ 写下 3 条失败日志
