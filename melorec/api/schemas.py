from pydantic import BaseModel
from typing import List, Optional

class HealthResponse(BaseModel):
    status: str

# --- THE UPDATED SCHEMA ---
class SongRecommendation(BaseModel):
    song_id: str
    title: str       # <-- ADD THIS LINE
    artist: str      # <-- ADD THIS LINE
    estimated_score: float

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[SongRecommendation]