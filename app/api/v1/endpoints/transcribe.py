# app/api/v1/endpoints/transcribe.py

from fastapi import APIRouter
from app.models.agent import TranscriptRequest, TranscriptResponse
from app.services import transcript_service

router = APIRouter()

@router.post("/create", response_model=TranscriptResponse)
async def create_transcript(request: TranscriptRequest):
    """
    Accepts a list of YouTube video URLs and returns their transcripts.
    """
    urls_as_strings = [str(url) for url in request.video_urls]
    
    # This line must call the function from the service file
    transcripts_data = await transcript_service.run_transcription_service(urls_as_strings)
    
    return {"transcripts": transcripts_data}