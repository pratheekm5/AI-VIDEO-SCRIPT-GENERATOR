# app/services/youtube_service.py

import asyncio
from typing import List, Optional

from fastapi import HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.config import settings
from app.models.agent import FetchedVideo

# The number of videos we want to return.
FINAL_VIDEO_COUNT = 1

def search_youtube_sync(query: str) -> List[FetchedVideo]:
    """
    Synchronous function that performs a single, cost-effective YouTube search.
    This uses only the 'search.list' endpoint (100 quota units).
    """
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            order="relevance",
            maxResults=FINAL_VIDEO_COUNT,
            relevanceLanguage="en",
            videoDefinition="high"
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId")
            if not video_id:
                continue
            
            video = FetchedVideo(
                url=f"https://www.youtube.com/watch?v={video_id}",
                title=snippet.get("title", "No Title"),
                thumbnail=snippet.get("thumbnails", {}).get("high", {}).get("url")
            )
            videos.append(video)
        return videos
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        raise HTTPException(status_code=e.resp.status, detail=f"YouTube API Error: {e.content.decode()}")

async def get_youtube_videos(topic: str, keywords: Optional[str]) -> List[FetchedVideo]:
    """
    Service function that finds relevant videos using a single, cost-effective API call.
    """
    if not settings.YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YOUTUBE_API_KEY is not configured.")
    
    # We still combine the topic and keywords for a better search query.
    # Using quotes around the topic helps prioritize it.
    search_terms = [f'"{topic}"']
    if keywords:
        search_terms.extend([kw.strip() for kw in keywords.split(',')])
    search_query = " ".join(search_terms)
    
    print(f"Searching YouTube with standard, low-cost query: '{search_query}'")

    try:
        # Run the single synchronous search function in a background thread.
        return await asyncio.to_thread(search_youtube_sync, search_query)
    except Exception as e:
        if not isinstance(e, HTTPException):
             raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
        raise e