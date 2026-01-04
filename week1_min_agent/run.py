from agent import ReActAgent
import openai

openai.api_key = "YOUR_API_KEY"

def llm_call(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # 或你能用的模型
        messages=messages,
        temperature=0
    )
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    agent = ReActAgent(llm_call)

    task = "What is (12 * 7) + 5?"
    running = True

    while running:
        running = agent.step(task)
        task = ""  # 后续轮次不再重复问题
