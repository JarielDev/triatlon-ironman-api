from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class DBActivity(Base):
    __tablename__ = "activities"

    # id interno de nuestra base de datos
    id = Column(Integer, primary_key=True, index=True) 
    strava_id = Column(Integer, unique=True, index=True) # <-- Agregamos unique=True

    # Los datos de tu entrenamiento
    name = Column(String, index=True)
    sport = Column(String)
    distance_km = Column(Float)
    moving_time_min = Column(Float)
    date = Column(String)