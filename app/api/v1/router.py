# app/api/v1/router.py

from fastapi import APIRouter
from app.api.v1.endpoints import agent, transcribe # 1. Import the new router

api_router = APIRouter()
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
# 2. Add the new router with its own prefix and tag
api_router.include_router(transcribe.router, prefix="/transcript", tags=["Transcription"])