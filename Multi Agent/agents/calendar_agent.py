from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools.calendar_tools import add_event, view_events

def create_calendar_agent():
    """
    Create agent powered by LLM. It has only calendar related tools.
    """