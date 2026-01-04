from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ShortTermMemory:
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    rejected_actions: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def record_action(self, tool, input):
        self.actions_taken.append({
            "tool": tool,
            "input": input
        })

    def record_observation(self, obs):
        self.observations.append(obs)

    def record_rejection(self, reason):
        self.rejected_actions.append(reason)

    def record_error(self, error):
        self.errors.append(error)

    def summary(self) -> str:
        """
        给模型看的“压缩版记忆”
        """
        parts = []

        if self.actions_taken:
            parts.append(
                "Actions taken: " +
                ", ".join(
                    f"{a['tool']}({a['input']})"
                    for a in self.actions_taken[-3:]
                )
            )

        if self.rejected_actions:
            parts.append(
                "Rejected actions: " +
                "; ".join(self.rejected_actions[-2:])
            )

        if self.errors:
            parts.append(
                "Errors: " +
                "; ".join(self.errors[-1:])
            )

        return "\n".join(parts)
