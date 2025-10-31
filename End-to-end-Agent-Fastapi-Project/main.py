from fastapi import FastAPI
from pydantic import BaseModel
from agent_core import get_agent_response
from typing import List

# --------------------------Define api request body and response body--------------------------------------
class QueryRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    answer: str
    tools_used: List[str] = []
    status: str
    error: str | None = None 

# -------------------------- FastAPI App initialize-------------------------------------------
app = FastAPI(
    title = 'LangChain AI Agent',
    description = 'A modular AI Agent API built with LangChain + FastAPI'
)

@app.get('/')
def health_check():
    return {"message": "LangChain AI Agent is running."}

@app.post('/ask', response_model = AgentResponse)
def ask_agent(request: QueryRequest):
    try:
        response_data = get_agent_response(request.query)
        return AgentResponse(
            answer = response_data["answer"],
            tools_used=response_data["tools_used"],
            status = response_data['status']
        )
    except Exception as e:
        return AgentResponse(
            answer="",
            tools_used=[],
            status="error",
            error=str(e)
        )