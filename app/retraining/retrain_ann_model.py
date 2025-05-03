import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Load sensor data
def load_sensor_data(csv_path):
    data = pd.read_csv(csv_path)
    X = data[["number_cars"]].values
    y = data["time_seconds"].values
    return X, y


# Retrain the ANN model
def retrain_model(csv_path, model_path, output_path):
    # Load data
    X, y = load_sensor_data(csv_path)

    # Preprocess data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Load existing model
    model = tf.keras.models.load_model(model_path)

    # Compile model
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])

    # Retrain model
    model.fit(
        X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32
    )

    # Save retrained model
    model.save(output_path)


if __name__ == "__main__":
    csv_path = "data/sensor_data.csv"
    model_path = "app/models/passing_time_ann/model.h5"
    output_path = "app/models/passing_time_ann/retrained_model.h5"

    retrain_model(csv_path, model_path, output_path)
