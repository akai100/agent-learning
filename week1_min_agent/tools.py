class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def execute(self, name, arg):
        if name not in self.tools:
            return f"Error: unknown tool '{name}'"
        try:
            return self.tools[name](arg)
        except Exception as e:
            return f"Tool error: {e}"


def calculator(expression: str) -> str:
    return str(eval(expression))
