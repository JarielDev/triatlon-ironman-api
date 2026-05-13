from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.strava_service import get_strava_activities  # Importamos tu nuevo servicio
from app.models import SyncResponse
from sqlalchemy.orm import Session 

#Importaciones para la base de datos
from app.database import engine, Base, SessionLocal
from app import db_models
from app.db_models import DBActivity




#SQLAlchemy que revise todos los DBModels 
# y cree el archivo .db con sus tablas si no existen.
Base.metadata.create_all(bind=engine)

# Función para manejar la conexión a la base de datos de forma segura
def get_db():
    db = SessionLocal() # Abre la puerta
    try:
        yield db        # Entrega la conexión a tu ruta para que la use
    finally:
        db.close()      # Cierra la puerta SIEMPRE, incluso si hay un error

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
async def sync_strava(db: Session = Depends(get_db)): # <-- Inyectamos la base de datos aquí
    # 1. Traemos los datos limpios de Strava
    activities = await get_strava_activities()
    
    actividades_nuevas = 0 # Contador para saber cuántas realmente guardamos hoy
    
    # 2. Guardamos cada actividad en la Base de Datos (con validación)
    for act in activities:
        
        # BUSCAMOS si ya existe una actividad con ese strava_id en la base de datos
        existe = db.query(DBActivity).filter(DBActivity.strava_id == act["strava_id"]).first()
        
        if not existe:
            # Creamos una "fila" SOLAMENTE si la actividad no estaba ya guardada
            nueva_actividad = DBActivity(
                strava_id=act["strava_id"],
                name=act["name"],
                sport=act["sport"],
                distance_km=act["distance_km"],
                moving_time_min=act["moving_time_min"],
                date=act["date"]
            )
            db.add(nueva_actividad) # La preparamos para guardar
            actividades_nuevas += 1
            
    db.commit() # ¡El guardado definitivo en el disco duro!
    
    # 3. Devolvemos la respuesta
    return {
        "message": f"Sincronización exitosa. Se guardaron {actividades_nuevas} actividades nuevas.",
        "total_activities": len(activities),
        "data": activities
    }