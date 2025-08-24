# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- THIS IS THE CRITICAL FIX ---
# Define the list of origins that are allowed to make requests.
# Your React app's URL must be in this list.
origins = [
    "http://localhost:3000", # Common for create-react-app
    "http://localhost:5173", # Common for Vite
    "http://localhost:5174", # Another common Vite port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# --- END OF FIX ---


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the AI YouTube Script Generator API!"}