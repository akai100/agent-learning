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

```init_chat_model``` 是一个非常关键的工厂函数（Utility Function）。它的核心作用是提供一种**供应商无关（Provider-agnostic）** 的方式来初始化聊天模型。

## 参数

+ model

  str，必填，模型的名称。

+ model_provider

  指定模型供应商。通常可以根据 model 自动推断

+ temperature

  控制随机性。越接近 0 越确定，越接近 1 越具创造性

+ max_tokens

  限制生成内容的最大 Token 数量

+ timeout

  设置请求超时时间。

+ max_retries

  请求失败后的重试次数

+ base_url

  自定义 API 端点（常用于中转站或本地私有化部署的模型，如 Ollama 或 vLLM）

+ api_key

  传入 API 密钥。如果未设置，默认从环境变量中读取（如 OPENAI_API_KEY）

+ streaming

  传入 API 密钥。如果未设置，默认从环境变量中读取（如 OPENAI_API_KEY）

+ configurable

  用于在 LangChain Expression Language (LCEL) 中进行动态配置
  
