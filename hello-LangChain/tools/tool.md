在 LangChain 中，@tool 装饰器是创建自定义工具最简单、也是最推荐的方式。它能将一个普通的 Python 函数瞬间转变为 LLM 可以理解并调用的“技能”。

只需在函数上方添加 @tool，LangChain 会自动解析函数名作为工具名，并将 Docstring（文档字符串） 作为工具描述。

```python3
from langchain.tools import tool

@tool
def calculate_repair_cost(parts_cost: float, labor_hours: float) -> str:
    """
    计算车辆维修的总费用。
    参数:
        parts_cost: 配件费用的金额。
        labor_hours: 预计维修所需的工时（每工时固定 200 元）。
    """
    total = parts_cost + (labor_hours * 200)
    return f"总维修预估费用为: {total} 元"

# 验证工具属性
print(calculate_repair_cost.name)  # 输出: calculate_repair_cost
print(calculate_repair_cost.description)  # 输出: 计算车辆维修的总费用...
```
