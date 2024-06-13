import numpy as np
import cv2 as cv

def hex_to_hsv(hex_color):
    """
    a tool to convert hex into its hsv value.
    source: chatGPT
    """
    # Convert HEX to RGB
    # remove the # from the beginning of the HEX string
    hex_color = hex_color.lstrip('#')
    # split the HEX string into its red, green, and blue
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # convert these components to integers
    rgb_color = np.uint8([[rgb_color]])  # create an array for OpenCV

    # Convert RGB to HSV
    hsv_color = cv.cvtColor(rgb_color, cv.COLOR_RGB2HSV)
    return hsv_color[0][0]
