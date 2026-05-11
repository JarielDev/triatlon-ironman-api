from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.strava_service import get_strava_activities  # Importamos tu nuevo servicio

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
@app.get("/strava-sync/")
async def sync_strava():
    try:
        # Llamamos a la función asíncrona que creaste
        data = await get_strava_activities()
        return {"message": "Sincronización exitosa con Strava", "total_activities": len(data), "data": data}
    except Exception as e:
        return {"error": str(e), "message": "Revisa tus credenciales en el archivo .env"}