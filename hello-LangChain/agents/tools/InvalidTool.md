在 LangChain 的代理架构中，```langchain.agents.tools.InvalidTool``` 是一个特殊的异常处理类，它在代理（Agent）试图调用一个不存在或名称拼写错误的工具时被触发。

## 解决问题

大模型在生成回复时，有时会产生幻觉：

+ 拼写错误： 比如你定义了工具 ```search_weather```，但模型输出 ```Action: weather_search```。

+ 臆造工具： 模型可能会根据直觉随口编造一个它认为“应该存在”但实际上你并没定义的工具。

如果没有 InvalidTool 机制，AgentExecutor 会因为找不到对应的工具函数而抛出 Python KeyError，导致整个程序中断。
