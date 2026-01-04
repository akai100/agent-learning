class AgentError(Exception):
    pass


class ParseError(AgentError):
    pass


class ToolError(AgentError):
    pass


class ValidationError(AgentError):
    pass
