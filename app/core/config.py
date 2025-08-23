# app/core/config.py

from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI YouTube Script Generator"
    API_V1_STR: str = "/api/v1"
    
    # The value from .env file will be a string. We need to parse it as a list.
    BACKEND_CORS_ORIGINS_STR: str = '[]'

    # Add the YouTube API Key field
    YOUTUBE_API_KEY: str = ""

    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        return json.loads(self.BACKEND_CORS_ORIGINS_STR)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()