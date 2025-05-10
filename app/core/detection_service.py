import numpy as np
import cv2
from ultralytics import YOLO
from collections import Counter


class DetectionService:
    def __init__(self, model_path):
        try:
            self.model = YOLO(model_path)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading the model: {e}")
            self.model = None

    def detect_cars(self, image):
        if self.model is None:
            print("Model is not loaded. Cannot perform detection.")
            return None

        try:
            # Resize image to 640x640 as YOLO expects
            image_resized = cv2.resize(image, (640, 640))

            # Run inference directly on (H, W, C) image
            results = self.model.predict(
                source=image_resized, save=False, verbose=False
            )

            print("Model inference completed!")

            # Get detections
            detections = results[0].boxes.cls.cpu().numpy()

            # Map class indices to names
            names = self.model.model.names

            # Define vehicle-related classes
            vehicle_classes = {
                "car",
                "bus",
                "motorbike",
                "pickup",
                "suv",
                "taxi",
                "truck",
                "van",
            }

            # Count occurrences of vehicle classes
            counts = Counter()
            for class_id in detections:
                label = names[int(class_id)]
                if label in vehicle_classes:
                    counts[label] += 1

            print("\nDetected vehicle counts:")
            for vehicle, count in counts.items():
                print(f"{vehicle}: {count}")

            return counts

        except Exception as e:
            print(f"Error during detection: {e}")
            return None
