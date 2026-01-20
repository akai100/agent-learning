
```python3
def create_react_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: BasePromptTemplate,
    output_parser: Optional[AgentOutputParser] = None,
    tools_renderer: ToolsRenderer = render_text_description,
    *,
    stop_sequence: Union[bool, list[str]] = True,
) -> Runnable:
    ......
```

它严格遵循 ReAct (Reasoning and Acting) 逻辑：模型先进行“思考”（Thought），再决定“行动”（Action），观察结果（Observation）后再继续。
