# app/api/v1/endpoints/agent.py

from fastapi import APIRouter
from app.models.agent import PortiaScriptRequest, PortiaScriptResponse
from app.services import agent_service

router = APIRouter()

@router.post("/create-script", response_model=PortiaScriptResponse)
async def create_portia_script(request: PortiaScriptRequest):
    """
    Accepts transcripts and user preferences, then uses the Portia SDK
    to generate a new, complete video script.
    """
    # Use .model_dump() to convert the Pydantic model to a dictionary
    # that we can pass to our service function.
    request_data = request.model_dump()
    
    final_script = await agent_service.generate_portia_script(request_data)
    
    return {"script": final_script}