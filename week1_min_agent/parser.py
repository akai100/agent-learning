import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentAction:
    tool: Optional[str]
    input: Optional[str]
    is_done: bool


class ReActParser:
    ACTION_RE = re.compile(r"Action:\s*(.*)")

    def parse(self, text: str) -> AgentAction:
        match = self.ACTION_RE.search(text)
        if not match:
            raise ValueError("No Action found in model output")

        action = match.group(1).strip()

        if action == "NONE":
            return AgentAction(None, None, True)

        if ":" not in action:
            raise ValueError(f"Invalid Action format: {action}")

        tool, arg = action.split(":", 1)
        return AgentAction(tool.strip(), arg.strip(), False)
