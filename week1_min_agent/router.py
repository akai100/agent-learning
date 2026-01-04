class ToolRouter:
    def __init__(self):
        self.allowed_tools = {
            "THINKING": [],
            "ACTING": ["calculator"],
        }

    def is_allowed(self, state, tool_name):
        allowed = self.allowed_tools.get(state.name, [])
        return tool_name in allowed
