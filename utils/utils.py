import cv2
import numpy as np


imageType = list[list[int]]


def convert_pictures_to_gray_scale_and_binary_array(path: str, res: int = 512) -> list[list[int]]:
    # Load the grayscale image array
    gray_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    gray_image = cv2.resize(gray_image, (res, res))
    # Apply the Sobel operator to detect edges
    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    # Compute the gradient magnitude
    gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    # Normalize the gradient magnitude for display
    gradient_magnitude_normalized = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    # threshold which convert edges to zero and one
    threshold = 47
    binary_array = np.where(gradient_magnitude_normalized <= threshold, 1, 0)
    return binary_array.tolist()


def save_image(pic_array: imageType) -> None:
    p_arr = np.array(pic_array)
    im = (p_arr * 255).astype(np.uint8)
    cv2.imwrite('temp.png', im)
