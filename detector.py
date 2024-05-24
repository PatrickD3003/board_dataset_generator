import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
import pytesseract
from PIL import Image
import re

def click_event(event, x, y, flags, param):
    """
    Function to display the coordinates of the points where mouse is clicked
    """
    if event == cv.EVENT_LBUTTONDOWN:  # Left button of the mouse is clicked
        print(x, ',', y)  # Print the coordinates of the point clicked


def mouse_callback(name, img):
    cv.namedWindow(name)  
    cv.setMouseCallback(name, click_event)
    # Display the image
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def crop_img(img):
    """
    divide the ROI(region of interest) into two part.
    one is the board part(to detect circles), 
    and one is the text above the board(to detect problem's name & grade).

    ensure indices are within the image size: 
    [row_start:row_end, col_start:col_end]
    """
    board_part = img[600:2332, 26:1124] 
    text_part = img[313:561, 13:1155]
    return board_part, text_part


def read_image(path):
    # Expand user path if it starts with ~
    path = os.path.expanduser(path)
    print(f"Reading image from: {path}")

    img = cv.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found at the path: {path}")
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv.blur(gray, (3, 3))

    return img


def blur_image(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))
    return gray_blurred


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


def remove_background_noise(colored_board):
    """
    using cv2.bitwise_and() between mask and the image
    to track a color, we define a mask in HSV color space using cv2.inRange()
    passing lower and upper limits of color values in HSV
    define a mask using np.zeros() 
    and slicing the entries with white(255) for the region in the input img

    use 3 masks:
    red mask to extract only red circles
    blue mask to extract only blue circles
    green mask to extract only green circles.
    """
    # Convert BGR to HSV
    # Hue: color type(ranging from 0 to 179)
    # Saturation: the intensity or purity of the color(ranging 0-255)
    # value: the brightness of the color (ranging 0-255)
    hsv = cv.cvtColor(colored_board, cv.COLOR_BGR2HSV)

    # HSV value for moonboard red #f44336
    hsv_red = hex_to_hsv("#f44336")
    # HSV value for moonboard blue #2961fe
    hsv_blue = hex_to_hsv("#2961fe")
    # HSV value for moonboard green #00c852
    hsv_green = np.array([62, 139, 197])


    # define range of red color in HSV
    lower_red = np.array([hsv_red[0] - 10, hsv_red[1] - 40, hsv_red[2] - 40])
    upper_red = np.array([hsv_red[0] + 10, hsv_red[1] + 40 ,hsv_red[2] + 40])

    # define range of blue color in HSV
    lower_blue = np.array([hsv_blue[0] - 10, hsv_blue[1] - 40, hsv_blue[2] - 40])
    upper_blue = np.array([hsv_blue[0] + 10, hsv_blue[1] + 40, hsv_blue[2] + 40])

    # define range of green color in HSV
    lower_green = np.array([hsv_green[0] - 10, hsv_green[1] - 40, hsv_green[2] - 40])
    upper_green = np.array([hsv_green[0] + 10, hsv_green[1] + 40, hsv_green[2] + 40]) 
    
    # create a mask
    red_mask = cv.inRange(hsv, lower_red, upper_red)
    blue_mask = cv.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    red_result = cv.bitwise_and(colored_board, colored_board, mask= red_mask)
    blue_result = cv.bitwise_and(colored_board, colored_board, mask= blue_mask)
    green_result = cv.bitwise_and(colored_board, colored_board, mask= green_mask)

    # display the mask and masked image
    # cv.imshow('Mask', blue_mask)
    # cv.waitKey(0)
    # cv.imshow('Masked Image', blue_result)
    # cv.waitKey(0)
    # cv.imshow('colored_board', colored_board)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return red_result, blue_result, green_result


def detect_circle(board_image):
    """
    1. input screenshot of a board.
    2. detect all the red, blue, green circles.
    3. return each central coordinate of the circle & its color.
    example:
    a = detect_circle(board_image)
    a = {"red":(x, y), "blue":(x, y), "blue":(x, y), "green":(x, y)}
    """
    # HoughCircles function requires a non-empty, single-channel (grayscale) image.
    # 1.ensure the input image is grayscale before calling 'HoughCircles'
    # 2.Add color detection logic to identify circles based on their colors.
    detected_circles = cv.HoughCircles(board_image, 
                                       cv.HOUGH_GRADIENT, 1, 20, param1 = 50,
                                       param2 = 30, minRadius = 50, maxRadius = 100)

    detected_coordinates = []
    
    if detected_circles is not None:
        # convert the circle parameters a, b, and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            detected_coordinates.append([a, b])
            # # Draw the circumference of the circle
            # # syntax : 
            # # cv2.circle(image, center_coordinates, radius, color, thickness)
            # cv.circle(board_image, (a, b), r, (255, 0, 0), 2)
            # # Draw a small circle (of radius 1) to show the center.
            # cv.circle(board_image, (a, b), 1, (255, 0, 0), 3)
            # print(a, b, r)
            # cv.imshow("Detected Circle", board_image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

    return detected_coordinates


def detect_text(text_image):
    """
    1. input screenshot of a text containing moonboard problem's name & grade
    2. detect the text.
    3. return both the problem's name and its grade.
    example:
    a = detect_text(text_image)
    a = ["Three combination", "V8"]
    """
    ocr_result = pytesseract.image_to_string(img)
    lines = ocr_result.split("\n")
    first_two_lines = lines[:2]

    cleaned_lines = []
    for i,line in enumerate(first_two_lines):
        if i ==0:
            cleaned_line = re.sub(r'^[^a-zA-Z]+', '', line)  # Remove leading non-alphabetic characters
            cleaned_line = re.sub(r'[^a-zA-Z]+$', '', cleaned_line)  # Remove trailing non-alphabetic characters
            cleaned_line = cleaned_line.strip()  # Remove leading and trailing whitespace
            
        if i ==1:
            match = re.search(r'\b[3-9][A-C]\+/V\d\b', line)
            cleaned_line = match.group(0) if match else ''
        cleaned_lines.append(cleaned_line)



    return cleaned_lines


def map_coordinates(board_coordinate):
    """
    1. input coordinate data from detect_circle()
    2. predict the type of holds based on the coordinate.
    3. return list of holds used in the screenshot
    example:
    a = map_coordinates(board_coordinate)
    a = {
    {start : False, goal : True, holds: J18},
    {start : False, goal : False, holds: E15},
    {start : False, goal : False, holds: D13},
    {start : True, goal : False, holds: A4}
    }
    """
    return None

if __name__ == "__main__":
    path = "/Users/wybeeboi/Documents/moonboard generator/board_dataset_generator/Resources/Photos/moonboard.PNG"
    img = read_image(path)
    colored_board, colored_text = crop_img(img)
    red_masked, blue_masked, green_masked =  remove_background_noise(colored_board)
    print(detect_text(colored_text))
    # blur each masks
    red_blurred = blur_image(red_masked)
    blue_blurred = blur_image(blue_masked)
<<<<<<< HEAD
    green_blurred = blur_image(green_masked)    
=======
    green_blurred = blur_image(green_masked)
>>>>>>> 793ff564429578df82f3f27ce0b0e9417b4725d0

    detect_red = detect_circle(red_blurred)
    detect_blue = detect_circle(blue_blurred)
    detect_green = detect_circle(green_blurred)

    print(detect_red)
    print(detect_blue)
    print(detect_green)
    
    # call the mouse_callback function with the cropped image part
    # mouse_callback("measurer", board_part)




