from parser import ReActParser

class Agent:
    def __init__(self, llm, tools, system_prompt, max_steps=5):
        self.llm = llm
        self.tools = tools
        self.parser = ReActParser()
        self.max_steps = max_steps

        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def run(self, task: str):
        self.messages.append({"role": "user", "content": task})

        for step in range(self.max_steps):
            print(f"\n=== Step {step + 1} ===")

            output = self.llm.call(self.messages)
            print(output)

            self.messages.append({"role": "assistant", "content": output})

            action = self.parser.parse(output)

            if action.is_done:
                print("\n✅ Agent finished")
                return

            observation = self.tools.execute(action.tool, action.input)
            obs_message = f"Observation: {observation}"

            print(obs_message)

            # Observation 是 system-level feedback
            self.messages.append(
                {"role": "system", "content": obs_message}
            )

        print("\n⛔ Max steps reached")
