# app/api/v1/endpoints/agent.py

from fastapi import APIRouter
from app.models.agent import VideoSearchRequest, VideoListResponse
from app.services import youtube_service

router = APIRouter()

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