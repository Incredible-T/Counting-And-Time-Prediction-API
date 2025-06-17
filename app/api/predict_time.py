from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.logger import logger
import cv2
import numpy as np
from app.core.detection_service import DetectionService
from app.core.passing_time import signal_controller_cycle
from config.firebase_store import store_data
import datetime

# import random


router = APIRouter()

detection_service = DetectionService("app/models/yolo11n.pt")


@router.post("/api/predict-time")
async def predict_time(file: UploadFile):
    logger.info(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    try:
        # Read the image file
        image_bytes = await file.read()
        logger.info(f"Size of uploaded file in bytes: {len(image_bytes)}")
        if not image_bytes:
            raise ValueError("Uploaded file is empty.")

        # Decode the image
        image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError(
                "Failed to decode image. Ensure the file is a valid image."
            )

        logger.info(f"Image successfully decoded. Shape: {image.shape}")

        # image = preprocess_image_for_yolo(image)

        # Detect cars
        car_count = detection_service.detect_cars(image)
        if car_count is None:
            raise HTTPException(
                status_code=500, detail="Failed to detect vehicles in the image."
            )
        # Convert Counter keys to strings or ints
        car_count_json_safe = dict(car_count)

        # call signal_controller_cycle
        pass_time = round(signal_controller_cycle(car_count_json_safe))

        # Generate random vehicle counts for comparison
        # random_car_count = {key: random.randint(0, 10) for key in car_count.keys()}

        # # Compare the generated random values with the detected car counts
        # logger.info(f"Generated random car count: {random_car_count}")
        # logger.info(f"Detected car count: {car_count_json_safe}")

        # # Update green time if the random car count is greater
        # if sum(random_car_count.values()) > sum(car_count_json_safe.values()):
        #     logger.info("Random car count is greater. Updating green time.")
        #     pass_time += pass_time * (1/3)

        # Store the data in Firebase
        store_data(
            "traffic_data",
            file.filename,
            {
                "vehicle_count_per_type": car_count_json_safe,
                "green_time": pass_time,
                "created_date": datetime.datetime.now().isoformat(),
            },
        )

        return {
            "vehicle_count_per_type": car_count_json_safe,
            "green_time": pass_time,
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error processing the image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing the image: {e}")
