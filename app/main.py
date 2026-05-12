from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.strava_service import get_strava_activities  # Importamos tu nuevo servicio
from app.models import SyncResponse

app = FastAPI(title="Triathlon Ironman Tracker")

class Workout(BaseModel):
    date: date
    sport: str
    distance: float
    duration_minutes: int
    feeling: Optional[str] = "Good"

my_workouts = []

@app.get("/")
def read_root():
    return {"message": "Road to Ironman 70.3 - Sistema Activo"}

@app.post("/workouts/")
def create_workout(workout: Workout):
    my_workouts.append(workout)
    return {"message": "Entrenamiento guardado con éxito", "workout": workout}

@app.get("/workouts/")
def get_workouts():
    return {"workouts": my_workouts}

# --- NUEVO ENDPOINT PARA STRAVA ---
# <-- Agregamos response_model=SyncResponse en esta línea
@app.get("/strava-sync/", response_model=SyncResponse) 
async def sync_strava():
    activities = await get_strava_activities()
    
    # Devolvemos el diccionario estructurado respetando el modelo
    return {
        "message": "Sincronización exitosa con Strava",
        "total_activities": len(activities),
        "data": activities
    }