在 LangGraph 中，**Graph（图）** 是最核心的概念。如果说传统的开发模式是“线性脚本”，那么 Graph 就是一套**有状态的、可循环的“工作流图纸”**。

你可以把 LangGraph 的 Graph 理解为一个**带有记忆的流程控制中心**。

## 图的三大支柱

理解 Graph，本质上是理解它的三个组成部分：

### State（状态）—— 图的共享账本

在 Graph 运行期间，所有数据都存储在一个名为 State 的对象中。

+ 特点

  每个节点（Node）都可以读取这个状态，修改它，然后传给下一个节点

+ 类比

  就像接力赛中的“接力棒”，但这个接力棒是个包，每个运动员（节点）都可以往里塞东西或拿东西。

### Nodes（节点）

节点本质上是 Python 函数

+ 输入

  当前的 State

+ 输出

  一个字典，用于更新 State

+ 类比

  流水线上的工位，负责处理特定的任务（如：调用 LLM、搜索数据库、处理格式）

### Edges (边) —— 图的“传送带”

边决定了数据从一个节点流向哪一个节点

+ **普通边**：直接从 A 到 B。

+ **条件边 (Conditional Edges)**：根据节点的输出结果（比如判断逻辑），决定下一步去哪。

+ **类比**：自动化工厂里的分拣传送带，根据产品的检测结果送往不同的包装口。

## Graph 的构建生命周期

构建一个 Graph 通常遵循以下“三步走”：

1. **定义 State**：确定你的图需要记住哪些信息（比如消息列表 messages）。

2. **添加 Nodes 和 Edges**：

```python3
builder = StateGraph(MyState)
builder.add_node("agent", call_model)
builder.add_node("tool", execute_tool)

# 设置入口、跳转逻辑和出口
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tool", "agent") # 循环回 agent
```

3. **编译 (Compile)**：将设计稿转化为可执行的 app

```python3
graph = builder.compile(checkpointer=memory)
```
