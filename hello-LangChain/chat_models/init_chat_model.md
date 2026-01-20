```python3
def init_chat_model(
    model: Optional[str] = None,
    *,
    model_provider: Optional[str] = None,
    configurable_fields: Optional[
        Union[Literal["any"], list[str], tuple[str, ...]]
    ] = None,
    config_prefix: Optional[str] = None,
    **kwargs: Any,
) -> Union[BaseChatModel, _ConfigurableModel]:
    ...
```

```init_chat_model``` 是一个非常关键的工厂函数（Utility Function）。它的核心作用是提供一种**供应商无关（Provider-agnostic）**的方式来初始化聊天模型。
