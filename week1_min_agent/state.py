from enum import Enum, auto

class AgentState(Enum):
    INIT = auto()
    THINKING = auto()
    ACTING = auto()
    OBSERVING = auto()
    RETRY = auto()
    DONE = auto()
    ERROR = auto()
