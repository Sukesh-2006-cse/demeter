from .base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def predict(self, query):
        return f"[Dummy Response] This is a placeholder answer for: {query}"
