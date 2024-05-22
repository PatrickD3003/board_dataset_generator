import cv2 as cv
import numpy as np

def get_hsv_value(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        hsv_value = param[y, x]
        print(f"HSV value at ({x}, {y}): {hsv_value}")

def analyze_hsv_values(image_path):
    # Load the image
    colored_board = cv.imread(image_path)
    hsv_image = cv.cvtColor(colored_board, cv.COLOR_BGR2HSV)

    # Display the image and set the callback function
    cv.imshow('Image', colored_board)
    cv.setMouseCallback('Image', get_hsv_value, param=hsv_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Provide the path to your image
image_path = '/Users/patrickdharma/Desktop/programming/openCV/moonboard_DatasetProject/Resources/Photos/moonboard.PNG'
analyze_hsv_values(image_path)
