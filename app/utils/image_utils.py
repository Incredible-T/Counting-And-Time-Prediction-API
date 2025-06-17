import cv2
import numpy as np


def preprocess_image_for_yolo(image):
    """
    Preprocess the image to resize it to 640x640 for YOLO model.

    Args:
        image (np.ndarray): Input image.

    Returns:
        np.ndarray: Preprocessed image ready for YOLO model.
    """

    # Check if the image is blurry
    def is_blurry(image, threshold=100.0):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var < threshold

    # Sharpen the image if it is blurry
    def sharpen_image(image):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    if is_blurry(image):
        image = sharpen_image(image)

    # Resize the image to 640x640
    resized_image = cv2.resize(image, (640, 640))

    # Normalize the image (scale pixel values to [0, 1])
    normalized_image = resized_image / 255.0

    # Convert image to the format expected by YOLO (channels first)
    preprocessed_image = np.transpose(normalized_image, (2, 0, 1))

    return preprocessed_image
