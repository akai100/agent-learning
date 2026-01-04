import openai

class OpenAILLM:
    def __init__(self, model="gpt-4o-mini", temperature=0):
        self.model = model
        self.temperature = temperature

    def call(self, messages):
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return resp["choices"][0]["message"]["content"]
