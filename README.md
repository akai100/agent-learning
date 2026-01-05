**第 1 周：LLM & Agent 基础认知**

**目标**

理解 Agent 是什么、能做什么、和普通 Chatbot 的区别。

**必学**

+ LLM 基本原理（Transformer / Token / Context）

+ Prompt 构成（System / User / Assistant）

+ ReAct 思想（Reason + Act）

+ OpenAI / Claude / 本地模型 API 调用

**实战**

+ 写一个 CLI Chatbot

+ 手写 ReAct Prompt

**产出**

+ ```react_chatbot.py```

+ 一篇笔记：《Agent ≠ Chatbot》

**第 2 周：Prompt Engineering & Reasoning**

**目标**

让模型“会思考、少胡说”。

**必学**

+ Chain of Thought

+ Self-Consistency

+ Prompt 模板化

+ 防 Prompt Injection

**实战**

+ 多版本 Prompt 对比实验

+ 设计一个“问题拆解 Prompt”

**产出**

+ Prompt 模板库

+ Prompt 实验报告

## 第 3 周：Agent 最小闭环（核心周）

### 目标

实现真正意义上的 Agent。

### 必学

+ Agent Loop：

```
Thought → Action → Observation → Thought
```


+ Tool Calling（Function Calling）

+ 状态管理

### 实战

+ 写一个 **不使用框架的 Agent**

+ Agent 可调用：

  + 搜索

  + 计算

  + 本地函数

### 产出

+ ```agent_core.py```

+ 一张 Agent 架构图

## 第 4 周：Planning（规划能力）

### 目标

让 Agent 能做「多步复杂任务」。

### 必学

+ Plan-and-Execute

+ Task Decomposition

+ Tree of Thoughts（概念 + 简化实现）

### 实战

+ 自动生成执行计划

+ 按计划逐步执行

### 产出

+ ```planner_agent.py```

+ 示例：自动完成一份调研任务

## 第 5 周：Memory & RAG

### 目标

让 Agent“记得住”。

### 必学

+ 短期 vs 长期记忆

+ Embedding 原理

+ 向量检索

+ RAG 设计模式

### 实战

+ 接入向量数据库（FAISS / Chroma）

+ Agent 可回忆历史信息

### 产出

+ ```memory_agent.py```

+ 一个「长期记忆 Agent」

## 第 6 周：LangChain / LangGraph（框架理解）

### 目标

能用框架，但不被框架限制。

### 必学

+ LangChain 抽象

+ LangGraph 状态图

+ Tool / Memory / Agent 封装

### 实战

+ 用 LangGraph 重写第 3 周 Agent

+ 对比手写 vs 框架

### 产出

+ LangGraph Agent Demo

+ 框架优缺点总结

## 第 7 周：Multi-Agent 系统

### 目标

让多个 Agent 协作。

### 必学

+ 角色拆分（Planner / Executor / Critic）

+ Agent 通信

+ 协作 / 投票 / 互评

### 实战

+ 3 Agent 协作完成复杂任务

+ 引入 Critic Agent

### 产出

+ ```multi_agent_system.py```

+ 协作流程图

## 第 8 周：Code Agent & Tool Agent

### 目标

让 Agent 真正“干活”。

### 必学

+ Code Generation + Execution

+ Sandbox

+ 工具失败恢复机制

**实战**

+ Code Agent 自动写并执行 Python

+ 文件 / API 操作 Agent

### 产出

+ Code Agent Demo

+ 自动 Debug 示例


## 第 9 周：评估、调试与稳定性

### 目标

让 Agent 稳定、可控、可复现。

### 必学

+ Agent Trace / Logging

+ 成功率评估

+ 幻觉检测

+ 回合成本控制

### 实战

+ 自动回归测试

+ 失败案例分析

### 产出

+ Agent Evaluation 脚本

+ Debug 面板（CLI / Web）

## 第 10 周：Self-Reflection & 自我改进

### 目标

让 Agent 变聪明。

### 必学

+ Reflection Prompt

+ Self-Refine

+ Critic Loop

### 实战

+ Agent 自我总结错误

+ 自动改进答案

### 产出

+ Self-Improving Agent Demo

## 第 11 周：安全、权限与工程化

### 目标

具备上线能力。

### 必学

+ Tool 权限控制

+ Prompt Injection 防御

+ 并发与限流

+ 成本优化

### 实战

+ 权限系统

+ Agent 行为白名单

### 产出

+ 安全 Agent 架构设计

## 第 12 周：最终项目（非常重要）

### 目标

证明你是 Agent 工程师。

### 项目选一

+ Auto Research Agent

+ 商业分析 Agent

+ Code Review Agent

+ AI 产品助理

### 要求

+ 多 Agent

+ Planning + Memory

+ 可评估

+ 可演示

### 产出

+ GitHub Repo

+ 技术文档

+ Demo 视频
