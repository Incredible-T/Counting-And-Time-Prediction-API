from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.storage_service import StorageService

router = APIRouter()

storage_service = StorageService("sensor_data.db")

class SensorData(BaseModel):
    number_cars: int
    time_seconds: float

@router.post("/api/sensor-data")
async def store_sensor_data(data: SensorData):
    try:
        storage_service.store_sensor_data(data.number_cars, data.time_seconds)
        return {"message": "Data stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing data: {e}")