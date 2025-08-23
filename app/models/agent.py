# app/models/agent.py

from pydantic import BaseModel, HttpUrl
from typing import Optional, List

# 1. Define the INPUT model for the POST request body
class VideoSearchRequest(BaseModel):
    topic: str
    keywords: Optional[str] = None
    video_language: Optional[str] = "en"

# 2. Define the OUTPUT model for a single video result
class FetchedVideo(BaseModel):
    url: HttpUrl
    title: str
    thumbnail: Optional[HttpUrl] = None

# 3. (Optional but good practice) Define the final response model
#    This helps if you want to add more data to the response later.
class VideoListResponse(BaseModel):
    videos: List[FetchedVideo]