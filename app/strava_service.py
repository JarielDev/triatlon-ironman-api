import httpx
import os
from dotenv import load_dotenv

load_dotenv() #Carga las varianbles del archivo .env

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# --- PRUEBA DE FUEGO ---
print("--- LEYENDO VARIABLES ---")
print(f"CLIENT_ID: {STRAVA_CLIENT_ID}")
print(f"SECRET CARGADO: {STRAVA_CLIENT_SECRET is not None}")
print(f"TOKEN CARGADO: {STRAVA_REFRESH_TOKEN is not None}")
print("-------------------------")

async def get_access_token():
    """Obtiene un token de acceso nuevo usando el refresh token."""
    url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET, #Secret Id, error común
        "refresh_token": STRAVA_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    
async def get_strava_activities():
    """Trae tus ultimas actividades de Strava"""
    token = await get_access_token()
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        raw_activities = response.json() # Aquí guardamos todo el JSON gigante

    cleaned_data = [
        {
            "name": activity["name"],
            "sport": activity["type"], 
            "distance_km": round(activity["distance"] / 1000, 2), # De metros a km, redondeado a 2 decimales
            "moving_time_min": round(activity["moving_time"] / 60, 2), # De segundos a minutos
            "date": activity["start_date_local"].split("T")[0] # Cortamos la fecha
        }
        for activity in raw_activities
    ]
    
    return cleaned_data