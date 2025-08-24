import re
import asyncio
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# --- YOUR ORIGINAL CODE, RESTORED AND CORRECTED ---

def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from a URL."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'embed\/([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Invalid YouTube URL: {url}")

def get_transcript_for_video(video_url: str, languages=['en']) -> str:
    """Return full transcript text of a YouTube video given its URL."""
    try:
        video_id = extract_video_id(video_url)
        
        # THIS IS THE CORRECT SYNTAX FOR YOUR INSTALLED LIBRARY VERSION
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=languages)
        
        # The .fetch() method in this version returns a list of objects, so we use .text
        return " ".join([snippet.text for snippet in transcript_data])
        
    except TranscriptsDisabled:
        print(f"❌ Transcripts are disabled for: {video_url}")
    except NoTranscriptFound:
        print(f"❌ No transcript found for: {video_url}")
    except Exception as e:
        print(f"⚠️ Unexpected error for {video_url}: {e}")
    return ""

def transcribe_multiple_videos(video_urls: List[str]) -> List[str]:
    """Transcribe multiple YouTube videos."""
    transcripts = []
    for url in video_urls:
        print(f"▶️ Transcribing video: {url}")
        transcript = get_transcript_for_video(url)
        transcripts.append(transcript)
    return transcripts

# --- MINIMAL API WRAPPER ---

async def run_transcription_service(video_urls: List[str]) -> List[str]:
    """
    This async function wraps your synchronous code to run it in a separate thread.
    """
    try:
        transcripts = await asyncio.to_thread(transcribe_multiple_videos, video_urls)
        return transcripts
    except Exception as e:
        print(f"An error occurred in the transcription service: {e}")
        return [f"ERROR: An error occurred processing the request. Check server logs."]