from state import AgentState
from router import ToolRouter
from parser import ReActParser
from memory import ShortTermMemory

class Agent:
    def __init__(self, llm, tools, system_prompt, max_steps=5):
        self.llm = llm
        self.tools = tools
        self.state = AgentState.INIT
        self.router = ToolRouter()
        self.selector = ToolSelector(self.router)
        self.parser = ReActParser()
        self.max_steps = max_steps
        self.memory = ShortTermMemory()
        self.retry_count = 0
        self.max_retries = 2

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
            memory_summary = self.memory.summary()
            if memory_summary:
                self.messages.append({
                    "role": "system",
                    "content": f"Short-term memory:\n{memory_summary}"
                })

            output = self.llm.call(self.messages)
            self.messages.append({"role": "assistant", "content": output})
            print(output)

            try:
                candidates = self.parser.parse(output)
            except Exception as e:
                self.memory.record_error(str(e))
                self.retry_count += 1
            
            if self.retry_count <= self.max_retries:
                print("🔁 Retry due to parse error")
                self.state = AgentState.RETRY
                continue
            else:
                self.state = AgentState.ERROR
                break

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

            try:
                observation = self.tools.execute(candidate.tool, candidate.input)
            except Exception as e:
                self.memory.record_error(str(e))
                self.retry_count += 1
                
                if self.retry_count <= self.max_retries:
                    print("🔁 Retry due to tool error")
                    self.state = AgentState.RETRY
                    continue
                else:
                    self.state = AgentState.ERROR
                    break

            obs_msg = f"Observation: {observation}"

            self.messages.append({"role": "system", "content": obs_msg})
            print(obs_msg)

            self.state = AgentState.THINKING

        print("\n⛔ Agent stopped | State:", self.state.name)
