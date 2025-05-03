# Count-Time Predict API

## Overview
The Count-Time Predict API is a machine learning-based project designed to predict the passing time of vehicles and detect cars using trained models. It provides APIs for prediction and sensor data processing, along with utilities for model retraining and data handling.

## Project Structure
```
LICENSE
README.md
requirements.txt
app/
    main.py
    api/
        predict_time.py
        sensor_data.py
    core/
        detection_service.py
        prediction_service.py
        storage_service.py
    models/
        car_detection/
            model.pth
        passing_time_ann/
            model.h5
    retraining/
        retrain_ann_model.py
    utils/
        github_utils.py
        image_utils.py
config/
    config.yaml
data/
    sensor_data.csv
docker/
    Dockerfile
logs/
    api.log
```

## Key Components
- **app/**: Contains the main application logic and API endpoints.
- **core/**: Core services for detection, prediction, and storage.
- **models/**: Pre-trained models for car detection and passing time prediction.
- **retraining/**: Scripts for retraining the ANN model.
- **utils/**: Utility scripts for GitHub integration and image processing.
- **config/**: Configuration files for the project.
- **data/**: Contains sensor data used for predictions.
- **docker/**: Dockerfile for containerizing the application.
- **logs/**: Log files for monitoring API activity.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Count-Time Predict API
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Access the API endpoints for predictions and sensor data processing.

## Retraining Models
To retrain the ANN model, use the script in the `retraining/` directory:
```bash
python retraining/retrain_ann_model.py
```

## License
This project is licensed under the terms specified in the `LICENSE` file.