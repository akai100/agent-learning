class ToolSelector:
    def __init__(self, router):
        self.router = router

    def validate(self, state, proposal):
        if proposal.is_done:
            return True, None

        if not self.router.is_allowed(state, proposal.tool):
            return False, f"Tool '{proposal.tool}' not allowed in state {state.name}"

        return True, None
