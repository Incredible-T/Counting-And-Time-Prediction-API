# Server Configuration
SERVER_URL = "http://localhost:8000/api/predict-time"
TIMEOUT_SECONDS = 10

# Camera Configuration
PHOTO_PATH = "images/traffic_photo.png"
CAMERA_COMMAND = "fswebcam -r 640x480 --no-banner {}"

# Traffic Light Timing
DEFAULT_GREEN_TIME = 10  # Default if server fails
YELLOW_TIME = 3
MIN_GREEN_TIME = 5
MAX_GREEN_TIME = 60

# GPIO Configuration
TRAFFIC_LIGHT_PINS = {
    "north": {"red": 21, "yellow": 20, "green": 16},
    "west": {"red": 24, "yellow": 23, "green": 18},
    "south": {"red": 22, "yellow": 27, "green": 17},
    "east": {"red": 13, "yellow": 6, "green": 5},
}

# System Configuration
DIRECTION_SEQUENCE = ["north", "west", "south", "east"]
ENABLE_PREFETCH = True
LOG_LEVEL = "INFO"

# Image mapping for each direction
DIRECTION_IMAGES = {
    "north": "images/north.png",
    "south": "images/south.png",
    "east": "images/east.png",
    "west": "images/west.png",
}
