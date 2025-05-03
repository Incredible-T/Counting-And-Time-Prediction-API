from fastapi import APIRouter, UploadFile, HTTPException
from app.core.detection_service import DetectionService
from app.core.prediction_service import PredictionService
import cv2
import numpy as np

router = APIRouter()

detection_service = DetectionService("app/models/car_detection/model.pth")
prediction_service = PredictionService("app/models/passing_time_ann/model.h5")

@router.post("/api/predict-time")
async def predict_time(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    try:
        # Read the image file
        image_bytes = await file.read()
        image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Detect cars
        car_count = detection_service.detect_cars(image)

        # Predict passing time
        estimated_time = prediction_service.predict_passing_time(car_count)

        return {"car_count": car_count, "estimated_passing_time_seconds": estimated_time}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {e}")