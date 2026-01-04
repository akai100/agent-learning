from state import AgentState
from parser import ReActParser
from selector import ToolSelector
from memory import ShortTermMemory


class Agent:
    def __init__(
        self,
        llm,
        tools,
        router,
        system_prompt,
        max_steps=8,
        max_retries=2,
    ):
        self.llm = llm
        self.tools = tools
        self.router = router
        self.selector = ToolSelector(router)
        self.parser = ReActParser()
        self.memory = ShortTermMemory()

        self.state = AgentState.INIT
        self.max_steps = max_steps
        self.max_retries = max_retries
        self.retry_count = 0

        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    # =========================
    # 主运行入口
    # =========================
    def run(self, task: str):
        print("\n🧠 Agent started")
        self.messages.append({"role": "user", "content": task})
        self.state = AgentState.THINKING

        for step in range(1, self.max_steps + 1):
            print(f"\n===== Step {step} | State: {self.state.name} =====")

            # 1️⃣ 注入短期 Memory（system-level）
            self._inject_memory()

            # 2️⃣ 调用 LLM
            output = self.llm.call(self.messages)
            self.messages.append({"role": "assistant", "content": output})
            print(output)

            # 3️⃣ 解析 Action Candidates
            try:
                candidates = self.parser.parse(output)
            except Exception as e:
                print("❌ Parse error:", e)
                self.memory.record_error(str(e))
                if not self._retry("Parse failed"):
                    break
                continue

            # 4️⃣ 选择 Action
            self.state = AgentState.ACTING
            candidate, reason = self.selector.select(self.state, candidates)

            if candidate is None:
                print("⛔ No valid action:", reason)
                self.memory.record_rejection(reason)
                if not self._retry(reason):
                    break
                continue

            # 5️⃣ 结束条件
            if candidate.is_done:
                self.state = AgentState.DONE
                print("\n✅ Agent finished successfully")
                return

            # 6️⃣ 执行工具
            try:
                print(f"🔧 Executing tool: {candidate.tool}({candidate.input})")
                observation = self.tools.execute(
                    candidate.tool,
                    candidate.input
                )
            except Exception as e:
                print("❌ Tool error:", e)
                self.memory.record_error(str(e))
                if not self._retry("Tool execution failed"):
                    break
                continue

            # 7️⃣ 记录 Memory
            self.memory.record_action(candidate.tool, candidate.input)
            self.memory.record_observation(observation)

            # 8️⃣ 注入 Observation（system-level）
            obs_msg = f"Observation: {observation}"
            self.messages.append(
                {"role": "system", "content": obs_msg}
            )
            print(obs_msg)

            # 9️⃣ 进入下一轮思考
            self.state = AgentState.THINKING
            self.retry_count = 0  # 成功后清空 retry

        print("\n⛔ Agent stopped | Final State:", self.state.name)

    # =========================
    # Retry 机制
    # =========================
    def _retry(self, reason: str) -> bool:
        self.retry_count += 1

        if self.retry_count > self.max_retries:
            self.state = AgentState.ERROR
            print("⛔ Max retries exceeded")
            return False

        print(f"🔁 Retry {self.retry_count}/{self.max_retries} | Reason: {reason}")
        self.state = AgentState.RETRY

        retry_hint = (
            "Previous attempt failed.\n"
            f"Reason: {reason}\n"
            "Do NOT repeat the same action.\n"
            "Propose a different and safer alternative."
        )

        self.messages.append(
            {"role": "system", "content": retry_hint}
        )

        self.state = AgentState.THINKING
        return True

    # =========================
    # Memory 注入
    # =========================
    def _inject_memory(self):
        summary = self.memory.summary()
        if summary:
            self.messages.append({
                "role": "system",
                "content": f"Short-term memory:\n{summary}"
            })
