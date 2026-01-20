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

## 高阶用法：处理复杂输入

如果你的工具参数非常复杂（例如需要验证日期格式、限制数值范围），建议配合 Pydantic 使用 args_schema 参数。

```python3
from pydantic import BaseModel, Field

class DamageInput(BaseModel):
    part_name: str = Field(description="受损部件名称，如 '前保险杠'")
    severity: int = Field(description="损毁程度，范围 1-10", ge=1, le=10)

@tool(args_schema=DamageInput)
def analyze_damage_logic(part_name: str, severity: int) -> str:
    """根据部件和损毁等级判定维修策略。"""
    if severity > 7:
        return f"{part_name} 损毁严重，建议更换。"
    return f"{part_name} 建议修复。"
```
