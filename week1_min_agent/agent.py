from state import AgentState
from router import ToolRouter
from parser import ReActParser

class Agent:
    def __init__(self, llm, tools, system_prompt, max_steps=5):
        self.llm = llm
        self.tools = tools
        self.state = AgentState.INIT
        self.router = ToolRouter()
        self.selector = ToolSelector(self.router)
        self.parser = ReActParser()
        self.max_steps = max_steps

        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def run(self, task: str):
        candidates = self.parser.parse(output)
        
        self.state = AgentState.ACTING
        
        candidate, reason = self.selector.select(self.state, candidates)
        
        if candidate is None:
            print("⛔ No valid action:", reason)
            self.state = AgentState.ERROR
            break
        
        if candidate.is_done:
            self.state = AgentState.DONE
            print("\n✅ Agent finished")
            return
        
        observation = self.tools.execute(candidate.tool, candidate.input)
        obs_msg = f"Observation: {observation}"
        
        self.messages.append(
            {"role": "system", "content": obs_msg}
        )
        print(obs_msg)
        
        self.state = AgentState.THINKING

        for step in range(self.max_steps):
            print(f"\n=== Step {step + 1} | State: {self.state.name} ===")

            output = self.llm.call(self.messages)
            self.messages.append({"role": "assistant", "content": output})
            print(output)

            proposal = self.parser.parse(output)

            if proposal.is_done:
                self.state = AgentState.DONE
                print("\n✅ Agent finished")
                return

            self.state = AgentState.ACTING

            ok, reason = self.selector.validate(self.state, proposal)
            if not ok:
                print("⛔ Action rejected:", reason)
                self.state = AgentState.ERROR
                break

            observation = self.tools.execute(action.tool, action.input)
            obs_msg = f"Observation: {observation}"

            self.messages.append({"role": "system", "content": obs_msg})
            print(obs_msg)

            self.state = AgentState.THINKING

        print("\n⛔ Agent stopped | State:", self.state.name)
