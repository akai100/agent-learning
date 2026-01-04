import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ActionCandidate:
    tool: Optional[str]
    input: Optional[str]
    is_done: bool


class ReActParser:
    ACTION_BLOCK_RE = re.compile(
        r"Action Candidates:(.*)", re.DOTALL
    )
    LINE_RE = re.compile(r"\d+\.\s*(.*)")

    def parse(self, text: str) -> List[ActionCandidate]:
        block_match = self.ACTION_BLOCK_RE.search(text)
        if not block_match:
            raise ValueError("No Action Candidates block found")

        block = block_match.group(1)
        lines = self.LINE_RE.findall(block)

        candidates = []

        for line in lines:
            line = line.strip()
            if line == "NONE":
                candidates.append(
                    ActionCandidate(None, None, True)
                )
                continue

            if ":" not in line:
                continue

            tool, arg = line.split(":", 1)
            candidates.append(
                ActionCandidate(tool.strip(), arg.strip(), False)
            )

        if not candidates:
            raise ValueError("No valid action candidates parsed")

        return candidates
