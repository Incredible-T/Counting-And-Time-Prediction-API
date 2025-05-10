import cv2
import numpy as np

def preprocess_image_for_yolo(image):
    """
    Preprocess the image to resize it to 640x640 for YOLO model.

    Args:
        image_path (str): Path to the input image.

    Returns:
        np.ndarray: Preprocessed image ready for YOLO model.
    """

    # Resize the image to 640x640
    resized_image = cv2.resize(image, (640, 640))

    # Normalize the image (scale pixel values to [0, 1])
    normalized_image = resized_image / 255.0

    # Convert image to the format expected by YOLO (channels first)
    preprocessed_image = np.transpose(normalized_image, (2, 0, 1))

    return preprocessed_image