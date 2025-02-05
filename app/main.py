from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()  # Carga las variables del archivo .env

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY no está configurada en el archivo .env")

EXCHANGE_API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair"

class SolicitudConversion(BaseModel):
    moneda_origen: str
    moneda_destino: str
    monto: float

async def obtener_tasa_de_cambio(moneda_origen: str, moneda_destino: str):
    """
    Obtiene la tasa de cambio desde la API de Exchange Rate.
    """
    url = f"{EXCHANGE_API_URL}/{moneda_origen}/{moneda_destino}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None  # Manejar error en caso de fallo en la API
        
        data = response.json()
        return data.get("conversion_rate")

@app.post("/convertir")
async def convertir_moneda(solicitud: SolicitudConversion):
    tasa = await obtener_tasa_de_cambio(solicitud.moneda_origen, solicitud.moneda_destino)
    
    if tasa is None:
        raise HTTPException(status_code=500, detail="Error al obtener la tasa de cambio")
    
    monto_convertido = solicitud.monto * tasa
    return {
        "moneda_origen": solicitud.moneda_origen,
        "moneda_destino": solicitud.moneda_destino,
        "monto": solicitud.monto,
        "monto_convertido": monto_convertido,
        "tasa_de_cambio": tasa
    }
