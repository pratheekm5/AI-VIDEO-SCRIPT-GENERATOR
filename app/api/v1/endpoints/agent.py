from fastapi import APIRouter
# 1. Import all necessary models and services
from app.models.agent import (
    PortiaScriptRequest, 
    PortiaScriptResponse,
    VideoSearchRequest,
    VideoListResponse
)
from app.services import agent_service, youtube_service

router = APIRouter()

# 2. Restore the missing /fetch-videos endpoint
@router.post("/fetch-videos", response_model=VideoListResponse)
async def fetch_youtube_videos(request: VideoSearchRequest):
    """
    Accepts a topic and keywords, searches YouTube for relevant videos,
    and returns a list of results.
    """
    videos_data = await youtube_service.get_youtube_videos(
        topic=request.topic,
        keywords=request.keywords
    )
    return {"videos": videos_data}


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