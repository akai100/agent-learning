class ToolSelector:
    def __init__(self, router):
        self.router = router

    def score(self, state, candidate):
        """
        简单评分规则（你可以不断进化它）
        """
        if candidate.is_done:
            return 100  # 优先结束

        if not self.router.is_allowed(state, candidate.tool):
            return -100

        # 偏好简单、安全工具
        score = 0

        if candidate.tool == "calculator":
            score += 10

        if candidate.tool == "search_stub":
            score += 5

        return score

    def select(self, state, candidates):
        scored = []

        for c in candidates:
            s = self.score(state, c)
            scored.append((s, c))

        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_candidate = scored[0]

        if best_score < 0:
            return None, "No acceptable action"

        return best_candidate, None
