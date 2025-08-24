from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
from typing import List

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
    video_id = extract_video_id(video_url)
    api = YouTubeTranscriptApi()  # ✅ v1.2.2 requires an instance
    try:
        # Fetch transcript (manually uploaded or auto-generated)
        transcript_data = api.fetch(video_id, languages=languages)
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

if __name__ == "__main__":
    youtube_links = [
        "https://www.youtube.com/watch?v=wysAcLUQBd0",
        "https://www.youtube.com/watch?v=BPKmkY_B8EI",
        "https://www.youtube.com/watch?v=rNxC16mlO60"
    ]
    
    transcripts = transcribe_multiple_videos(youtube_links)
    
    for i, text in enumerate(transcripts, start=1):
        print(f"\nTranscript for video {i}:\n{text}\n")
