import tensorflow as tf
import numpy as np
import cv2

class DetectionService:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def detect_cars(self, image):
        # Preprocess the image
        image_resized = cv2.resize(image, (224, 224))  # Example size
        image_normalized = image_resized / 255.0
        image_batch = np.expand_dims(image_normalized, axis=0)

        # Predict car presence
        predictions = self.model.predict(image_batch)
        car_count = int(np.sum(predictions > 0.5))  # Example threshold
        return car_count