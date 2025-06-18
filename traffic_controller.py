import time
import requests
import os
import logging
from itertools import cycle
import threading
from gpiozero import LED
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

# Import configuration
from config.config import (
    LOG_LEVEL,
    DEFAULT_GREEN_TIME,
    DIRECTION_SEQUENCE,
    TRAFFIC_LIGHT_PINS,
    PHOTO_PATH,
    CAMERA_COMMAND,
    ENABLE_PREFETCH,
    MIN_GREEN_TIME,
    MAX_GREEN_TIME,
    YELLOW_TIME,
    SERVER_URL,
    TIMEOUT_SECONDS,
    DIRECTION_IMAGES,
)

# Use MockFactory for non-Raspberry Pi systems
Device.pin_factory = MockFactory()

# Setup basic logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global Variables for Pre-fetching
next_green_times = {}
prefetch_lock = threading.Lock()


class TrafficController:
    def __init__(self):
        self.setup_gpio()
        self.direction_cycle = cycle(DIRECTION_SEQUENCE)
        self.current_direction = next(self.direction_cycle)

        # Ensure all required images exist
        for direction, image_path in DIRECTION_IMAGES.items():
            if not os.path.exists(image_path):
                logging.error(f"Missing image for {direction}: {image_path}")
                raise FileNotFoundError(f"Required image not found: {image_path}")

    def setup_gpio(self):
        """Initialize GPIO pins using gpiozero"""
        self.leds = {}
        for direction in TRAFFIC_LIGHT_PINS:
            self.leds[direction] = {
                "red": LED(TRAFFIC_LIGHT_PINS[direction]["red"]),
                "yellow": LED(TRAFFIC_LIGHT_PINS[direction]["yellow"]),
                "green": LED(TRAFFIC_LIGHT_PINS[direction]["green"]),
            }
        logging.info("GPIO pins initialized using gpiozero")

    def all_red(self):
        """Turn all lights to red"""
        for direction in self.leds:
            self.leds[direction]["red"].on()
            self.leds[direction]["yellow"].off()
            self.leds[direction]["green"].off()

    def capture_image(self):
        """Capture image from camera"""
        try:
            os.makedirs(os.path.dirname(PHOTO_PATH), exist_ok=True)
            cmd = CAMERA_COMMAND.format(PHOTO_PATH)
            result = os.system(cmd)

            if result == 0 and os.path.exists(PHOTO_PATH):
                logging.info("Image captured successfully")
                return True
            else:
                logging.error("Failed to capture image")
                return False
        except Exception as e:
            logging.error(f"Camera error: {e}")
            return False

    def request_green_time(self, direction):
        """Request green time from prediction server"""
        logging.info(f"Requesting green time for {direction.upper()}")

        if not self.capture_image():
            return DEFAULT_GREEN_TIME

        try:
            # Use the pre-captured image for the current direction
            # image_path = DIRECTION_IMAGES[direction]

            # Read the image file
            with open(PHOTO_PATH, "rb") as image_file:
                files = {
                    "file": (
                        os.path.basename(PHOTO_PATH),
                        image_file,
                        "image/jpeg",
                    )
                }
                logging.info(f"Sending request to {SERVER_URL} with image {PHOTO_PATH}")
                response = requests.post(
                    SERVER_URL,
                    files=files,
                    timeout=TIMEOUT_SECONDS,
                    headers={"content_type": "multipart/form-data"},
                )

            response.raise_for_status()
            data = response.json()
            green_time = int(data.get("green_time", DEFAULT_GREEN_TIME))

            # Validate green time bounds
            green_time = max(MIN_GREEN_TIME, min(MAX_GREEN_TIME, green_time))

            logging.info(f"Server response for {direction.upper()}: {green_time}s")
            return green_time

        except requests.exceptions.Timeout:
            logging.error(
                f"Server timeout for {direction.upper()} - request took longer than 30 seconds"
            )
            return DEFAULT_GREEN_TIME
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error for {direction.upper()}: {str(e)}")
            if hasattr(e.response, "text"):
                logging.error(f"Server response: {e.response.text}")
            return DEFAULT_GREEN_TIME
        except Exception as e:
            logging.error(f"Unexpected error for {direction.upper()}: {str(e)}")
            return DEFAULT_GREEN_TIME

    def prefetch_next_green_time(self, next_direction):
        """Pre-fetch green time for next direction in background"""
        if not ENABLE_PREFETCH:
            return

        def fetch_in_background():
            try:
                green_time = self.request_green_time(next_direction)
                with prefetch_lock:
                    next_green_times[next_direction] = green_time
                    logging.info(f"Pre-fetched {next_direction.upper()}: {green_time}s")
            except Exception as e:
                logging.error(f"Pre-fetch failed for {next_direction.upper()}: {e}")

        thread = threading.Thread(target=fetch_in_background, daemon=True)
        thread.start()

    def get_green_time(self, direction):
        """Get green time - either from cache or request new"""
        with prefetch_lock:
            if direction in next_green_times:
                green_time = next_green_times.pop(direction)
                logging.info(
                    f"Using cached green time for {direction.upper()}: {green_time}s"
                )
                return green_time

        logging.info(f"No cached data, requesting live for {direction.upper()}")
        return self.request_green_time(direction)

    def activate_sequence(self, direction, green_time, next_direction=None):
        """Activate traffic light sequence"""
        # Turn on all red lights first
        for dir_key in self.leds:
            self.leds[dir_key]["red"].on()
            self.leds[dir_key]["yellow"].off()
            self.leds[dir_key]["green"].off()

        leds = self.leds[direction]

        # Green phase - turn off red light only for current direction
        leds["red"].off()
        leds["green"].on()
        logging.info(f"GREEN: {direction.upper()} for {green_time}s")

        # Start pre-fetching next direction
        if next_direction and ENABLE_PREFETCH:
            self.prefetch_next_green_time(next_direction)

        time.sleep(green_time)

        # Yellow phase
        leds["green"].off()
        leds["yellow"].on()
        logging.info(f"YELLOW: {direction.upper()} for {YELLOW_TIME}s")
        time.sleep(YELLOW_TIME)

        # Red phase - turn on red light for current direction
        leds["yellow"].off()
        leds["red"].on()
        logging.info(f"RED: {direction.upper()}")

    def get_next_direction(self):
        """Get the next direction in sequence"""
        try:
            current_index = DIRECTION_SEQUENCE.index(self.current_direction)
            next_index = (current_index + 1) % len(DIRECTION_SEQUENCE)
            return DIRECTION_SEQUENCE[next_index]
        except ValueError:
            return DIRECTION_SEQUENCE[0]

    def run(self):
        """Main traffic control loop"""
        logging.info("Starting AI-Driven Traffic Light System")
        self.all_red()
        time.sleep(2)  # Initial safety delay

        try:
            while True:
                next_direction = self.get_next_direction()
                green_time = self.get_green_time(self.current_direction)

                self.activate_sequence(
                    self.current_direction, green_time, next_direction
                )

                self.current_direction = next(self.direction_cycle)

        except KeyboardInterrupt:
            logging.info("Manual shutdown initiated")
        except Exception as e:
            logging.error(f"System error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up GPIO and resources"""
        self.all_red()
        time.sleep(1)
        for direction in self.leds:
            for led in self.leds[direction].values():
                led.off()
        logging.info("System shutdown complete")


if __name__ == "__main__":
    controller = TrafficController()
    controller.run()
