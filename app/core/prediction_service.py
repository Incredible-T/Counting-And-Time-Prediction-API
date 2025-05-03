import tensorflow as tf

class PredictionService:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict_passing_time(self, car_count):
        # Predict passing time based on car count
        prediction = self.model.predict([[car_count]])
        return float(prediction[0][0])