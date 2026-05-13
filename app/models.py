from pydantic import BaseModel
from typing import List

class StravaActivity(BaseModel):
    strava_id: int
    name: str
    sport: str
    distance_km: float
    moving_time_min: float
    date: str

class SyncResponse(BaseModel):
    message: str
    total_activities: int
    data: List[StravaActivity]