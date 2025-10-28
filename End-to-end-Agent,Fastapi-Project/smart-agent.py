'''
We are creating a multi-tool AI Agent.
'''

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, AgentType

from dotenv import load_dotenv
import os


# ----------------------- Load API key------------------------------------------------------------
load_dotenv('config.env')
api_key = os.getenv('OPENAI_API_KEY')

# Create LLM instance
llm = ChatOpenAI(model= 'gpt-4o-mini', api_key = api_key)

# ----------------------------------------Define tools-------------------------------------------------

@tool
def add_numbers(a:float, b:float) -> float:
    return a+b

@tool
def summarize(text:str) -> str:
    """Summarize given text in 2-3 sentences."""
    if len(text.split()) < 30:
        return "Text is too short to summarize."
    prompt = f"Summarize this text in 2-3 sentence:{text}"
    summary_response = llm.invoke(prompt)
    return summary_response.content

search = DuckDuckGoSearchRun()

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

#---------------------------------List tools available to agent------------------------------
tools = [add_numbers, summarize, search, wiki]

# --------------------------------Initialize Agent-------------------------------------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -------------------------------Function to call the Agent----------------------------------
def get_agent_response(query:str) -> str:
    response = llm.invoke({"input":query})
    return response['output']