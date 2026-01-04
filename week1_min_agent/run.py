from agent import Agent
from llm import OpenAILLM
from tools import ToolRegistry, calculator
from prompt import SYSTEM_PROMPT
import openai

openai.api_key = "YOUR_API_KEY"

tools = ToolRegistry()
tools.register("calculator", calculator)

llm = OpenAILLM()
agent = Agent(llm, tools, SYSTEM_PROMPT)

agent.run("What is (12 * 7) + 5?")
