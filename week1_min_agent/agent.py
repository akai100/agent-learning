import re
from prompt import SYSTEM_PROMPT
from tools import TOOLS

class ReActAgent:
  def __init__(self, llm_call):
    self.llm_call = llm_call
    self.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

  def parse_action(self, text: str):
    match = re.search(r"Action:\s*(.*)", text)
    if not match:
      return None, None

    action = match.group(1).strip()
    if action == "NONE":
      return "NONE", None

    if ":" in action:
      tool, arg = action.split(":", 1)
      return tool.strip(), arg.strip()

    return None, None

def step(self, user_input: str):
    self.messages.append({"role": "user", "content": user_input})
    response = self.llm_call(self.messages)

    self.messages.append({"role": "assistant", "content": response})
    print("\nAgent Output:\n", response)

    tool_name, tool_input = self.parse_action(response)

    if tool_name == "NONE":
        return False  # 结束

    if tool_name in TOOLS:
        observation = TOOLS[tool_name](tool_input)
    else:
        observation = f"Unknown tool: {tool_name}"

    # 把 Observation 喂回模型
    obs_text = f"Observation: {observation}"
    self.messages.append({"role": "user", "content": obs_text})
    print("\nObservation:\n", observation)

    return True  # 继续
