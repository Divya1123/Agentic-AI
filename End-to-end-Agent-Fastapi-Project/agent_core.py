'''
We are creating a multi-tool AI Agent.
'''
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from dotenv import load_dotenv
import os


# ----------------------- Load API key------------------------------------------------------------
load_dotenv('config.env')
api_key = os.getenv('OPENAI_API_KEY')

# Create LLM instance
llm = ChatOpenAI(model= 'gpt-4o-mini', api_key = api_key)

# ----------------------------------------Define tools-----------------------------------------------

@tool
def add_numbers(a:float, b:float) -> float:
    """Adds two numbers and returns the result."""
    return a+b

@tool
def summarize(text:str) -> str:
    """Summarizes a long text into a short form."""
    if len(text.split()) < 30:
        return "Text is too short to summarize."
    prompt = f"Summarize this text in 2-3 sentence:{text}"
    summary_response = llm.invoke(prompt)
    return summary_response.content

search = DuckDuckGoSearchRun()

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# --------------------------------List tools available to agent---------------------------------------
tools = [add_numbers, summarize, search, wiki]

# ----------------------- Prompt -----------------------
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant that can use tools to answer questions.
Use tools when needed and provide a clear, accurate final answer.

User input: {input}
{agent_scratchpad}
""")

# --------------------------------Initialize Agent----------------------------------------------------
from langchain.agents import create_openai_functions_agent, AgentExecutor

agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

executor = AgentExecutor(
    agent=agent, 
    tools=tools,
    handle_parsing_errors=True,
    verbose=True,
    max_iterations=8
)

# -------------------------------Function to call the Agent-------------------------------------------
from langchain.callbacks.base import BaseCallbackHandler

def get_agent_response(query:str):
    "Run query via langchain agent"
    tool_calls = []

    class ToolUsageTracker(BaseCallbackHandler):
        def on_tool_start(self, serialized, input_str, **kwargs):
            tool_calls.append(serialized.get("name", "UnknownTool"))
        
    tracker = ToolUsageTracker()

    try:
        response = executor.invoke({"input": query}, config={"callbacks": [tracker]})
        return {
            "answer":response.get("output", ""),
            "tools_used": list(set(tool_calls)),
            "status": "success"
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "tools_used": [],
            "status": "error"
        }