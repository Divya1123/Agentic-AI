from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from agent_tools import get_agent_tools
import os

load_dotenv('config.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

def llm_response(user_query):

    model = init_chat_model(
        'gpt-4o',
        model_provider = 'openai',
        api_key = openai_api_key
    )

    # fetch tools
    tools = get_agent_tools

    # bind the tools to the model
    model_with_tools = model.bind_tools(tools)

    # send user query
    response = model_with_tools.invoke([
        {
            "role" : "user",
            "content" : user_query
        }
    ])

    print(f"Message content: {response.text()}\n")
    print(f"Tool calls: {response.tool_calls}")