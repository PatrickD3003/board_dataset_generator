import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
import pytesseract
import easyocr
import re
from database.database import data_to_database
from tools.hex_to_hsv import hex_to_hsv

#  色のHSV値の初期化
HSV_RED = hex_to_hsv("#f44336")
HSV_BLUE = hex_to_hsv("#2961fe")
HSV_GREEN = np.array([62, 139, 197])
HSV_YELLOW = [27, 141, 235]
HSV_BLACK = [120, 8, 32]


def crop_img(img):
    """
    divide the ROI(region of interest) into two part.
    one is the board part(to detect circles), 
    and one is the text above the board(to detect problem's name & grade).

    ensure indices are within the image size: 
    [row_start:row_end, col_start:col_end]
    """
    board_part = img[600:2332, 26:1124] 
    text_part1 = img[328:582, 151:1049]
    # cv.imshow('text', text_part)
    # cv.waitKey(0)
    return board_part, text_part1


def read_image(path):
    # Expand user path if it starts with ~
    path = os.path.expanduser(path)
    print(f"Reading image from: {path}")  # **debug purpose**
    img = cv.imread(path)
    if img is None:
        None
    else:
        # Proceed with your image processing tasks
        print("Image loaded successfully.")

    return img


def blur_image(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))
    return gray_blurred


def remove_background_noise(colored_board, hsv_value):
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
    # define range of the color in hsv value
    lower = np.array([hsv_value[0] - 10, hsv_value[1] - 40, hsv_value[2] - 40])
    upper = np.array([hsv_value[0] + 10, hsv_value[1] + 40 ,hsv_value[2] + 40])
    # create a mask
    mask = cv.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    result = cv.bitwise_and(colored_board, colored_board, mask= mask)

    # # display the mask and masked image
    # cv.imshow('Mask', mask)
    # cv.waitKey(0)
    # cv.imshow('Masked Image', result)
    # cv.waitKey(0)
    # cv.imshow('colored_board', colored_board)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return result


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


def detect_text(text_image1):
    """
    1. input screenshot of a text containing moonboard problem's name & grade
    2. detect the text.
    3. return both the problem's name and its grade.
    example:
    a = detect_text(text_image)
    a = ["Three combination", "V8"]
    """

    reader = easyocr.Reader(['en'])  # Specify language(s)
    result = reader.readtext(text_image1)
    text2 = ' '.join([item[1] for item in result])

    text1 = pytesseract.image_to_string(text_image1)
    # print(text1)  # **for debugging purpose**
    first_two_lines = []
    first_two_lines.append(text1[0])
    lines = text1.split("\n")
    first_two_lines = lines[:2]

    cleaned_lines = []
    text2 = text2.replace("Z","7")
    for i,line in enumerate(first_two_lines):
        if i ==0:
            match = re.search(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*|\d+[a-zA-Z]+|[a-zA-Z]+\d+', line)
            cleaned_line = match.group(0) if match else ''      
            
        if i ==1:
            match = re.search(r'\b[5-9][A-Z]\+?\/V?(1[0-9]|20|[1-9])\b',text2)
            cleaned_line = match.group(0).replace('/',"/V") if 'V' not in match.group(0) else match.group(0) 

        cleaned_lines.append(cleaned_line)


    return cleaned_lines


def map_coordinates(coordinates, color):
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
    # define the labels.
    hold_labels_column = list("ABCDEFGHIJK")
    hold_labels_row = [i for i in range(18, 0, -1)]
    # a list containing all the labels detected from the coordinates
    hold_labels = []
    # pick sample hold's coordination
    # (column, row)
    A18_coordinate = (142, 128)
    B18_coordinate = (232, 128)
    A17_coordinate = (142, 218)
    # count the distance between holds, both the column and row
    column_distance = B18_coordinate[0] - A18_coordinate[0]
    row_distance = A17_coordinate[1] - A18_coordinate[1]

    for coordinate in coordinates:
        column_label = ""
        row_label = ""
        # check column
        i = 0
        while (i < len(hold_labels_column)):
            column_scan = A18_coordinate[0] + column_distance * i
            if (column_scan - 10) <= coordinate[0] <= (column_scan + 10):
                column_label = hold_labels_column[i]
                break
            i += 1

        # check row
        i = 0
        while (i < len(hold_labels_row)):
            row_scan = A18_coordinate[1] + row_distance * i
            if (row_scan - 40) <= coordinate[1] <= (row_scan + 40):
                row_label = hold_labels_row[i]
                break
            i += 1
        
        # create the (column + row) label 
        label = column_label + str(row_label)
        hold_labels.append(label)

    return hold_labels


def run_detector(path=f"Resources/Photos/TESTRUN/test.PNG", grade="VTest"):
    """
    a function that summarize the detection process
    return the problem's name & grade & the holds position.
    """
    # read image, separate into two ROI, board and text.
    img = read_image(path)
    if img is None:
        print(f"Failed to load img")
    else:
        colored_board, colored_text = crop_img(img)
        # red_masked, blue_masked, green_masked =  remove_background_noise(colored_board)
        red_masked = remove_background_noise(colored_board, HSV_RED)
        blue_masked = remove_background_noise(colored_board, HSV_BLUE)
        green_masked = remove_background_noise(colored_board, HSV_GREEN)
        # blur each masks
        red_blurred = blur_image(red_masked)
        blue_blurred = blur_image(blue_masked)
        green_blurred = blur_image(green_masked)    
        # detect the circle's color and its coordinate
        detect_red = detect_circle(red_blurred)
        detect_blue = detect_circle(blue_blurred)
        detect_green = detect_circle(green_blurred)
        # detect the boulder's name and its grade, return a list
        text_image = detect_text(colored_text)
        # map each coordinate into moonboard hold labels
        red_labels = map_coordinates(detect_red, "red")
        blue_labels = map_coordinates(detect_blue, "blue")
        green_labels = map_coordinates(detect_green, "green")

        print(text_image, red_labels, blue_labels, green_labels, sep="\n")

        # input to database
        data_to_database(text_image, red_labels, blue_labels, green_labels, grade)


def list_item_in_folder(folder_path):
    """
    function to count number of items in a directory,
    excluding the hidden files
    """
    # List all items in the directory, count how many files inside
    items = os.listdir(folder_path)
    # exclude hidden and system files
    items = [item for item in items if item != '.DS_Store']
    count = len(items)

    return count


def scan_all(grade):
    """
    a function to scan whole file in a directory.
    for example, scan_all("V3") will open V3 folder,
    scan everything inside and put it in database.
    """
    # define the folder's path
    folder_path = f"Resources/Photos/{grade}"
    # count number of files with list_item_in_folder() function
    count = list_item_in_folder(folder_path)

    # use run_detector function on all files 
    for num in range(count):
        file_path = folder_path + f"/{grade}_{num+1}.PNG"
        run_detector(file_path, grade)


if __name__ == "__main__":
    scan_all("V4")
    # call the mouse_callback function with the cropped image part
    # mouse_callback("measurer", board_part)




