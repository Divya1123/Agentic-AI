from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv('config.env')

user_query = 'what is the weather in SF'

def get_agent_tools():
    tavily_key = os.getenv('TAVILY_API_KEY')
    search_tool = TavilySearch(tavily_api_key = tavily_key, max_results=2)
    # return list of tool objects
    return [search_tool]