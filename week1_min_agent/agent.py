from state import AgentState
from router import ToolRouter
from parser import ReActParser

class Agent:
    def __init__(self, llm, tools, system_prompt, max_steps=5):
        self.llm = llm
        self.tools = tools
        self.state = AgentState.INIT
        self.router = ToolRouter()
        self.parser = ReActParser()
        self.max_steps = max_steps

        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def run(self, task: str):
        self.messages.append({"role": "user", "content": task})
        self.state = AgentState.THINKING

        for step in range(self.max_steps):
            print(f"\n=== Step {step + 1} | State: {self.state.name} ===")

            output = self.llm.call(self.messages)
            self.messages.append({"role": "assistant", "content": output})
            print(output)

            try:
                action = self.parser.parse(output)
            except Exception as e:
                print("❌ Parse error:", e)
                self.state = AgentState.ERROR
                break

            if action.is_done:
                self.state = AgentState.DONE
                print("\n✅ Agent finished")
                return

            self.state = AgentState.ACTING

            if not self.router.is_allowed(self.state, action.tool):
                print(f"⛔ Tool '{action.tool}' not allowed in state {self.state.name}")
                self.state = AgentState.ERROR
                break

            observation = self.tools.execute(action.tool, action.input)
            obs_msg = f"Observation: {observation}"

            self.messages.append({"role": "system", "content": obs_msg})
            print(obs_msg)

            self.state = AgentState.THINKING

        print("\n⛔ Agent stopped | State:", self.state.name)
