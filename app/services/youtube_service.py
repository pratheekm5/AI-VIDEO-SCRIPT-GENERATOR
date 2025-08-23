import asyncio
from app.models.agent import FetchedVideo
from typing import List, Optional
from app.core.config import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

async def get_youtube_videos(topic: str, keywords: Optional[str]) -> List[FetchedVideo]:
    """
    This service function uses the YouTube Data API v3 to search for videos.
    """
    if not settings.YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY is not configured in the .env file.")
    
    search_terms = [topic]
    if keywords:
        search_terms.extend([kw.strip() for kw in keywords.split(',')])
    search_query = " ".join(search_terms)
    print(f"Searching YouTube with improved query: '{search_query}'")

    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: search_youtube_sync(search_query)
        )
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def search_youtube_sync(query: str) -> List[FetchedVideo]:
    """
    Synchronous function that performs the YouTube search.
    """
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    filtered_query = f"{query} -#shorts"
    request = youtube.search().list(
        part="snippet",
        q=filtered_query,
        type="video",
        order="viewCount",
        videoCaption="closedCaption",
        maxResults=1,
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
