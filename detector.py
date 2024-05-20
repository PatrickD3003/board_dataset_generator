import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os

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
    text_part = img[328:514, 291:889]
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

    return img, gray_blurred

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
    
    if detected_circles is not None:
        # convert the circle parameters a, b, and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # need to determine the color of the circle

            # Draw the circumference of the circle
            cv.circle(board_image, (a, b), r, (0, 255, 0), 2)
            # Draw a small circle (of radius 1) to show the center.
            cv.circle(board_image, (a, b), 1, (0, 0, 255), 3)

            cv.imshow("Detected Circle", board_image)
            cv.waitKey(0)
            cv.destroyAllWindows()


def detect_text(text_image):
    """
    1. input screenshot of a text containing moonboard problem's name & grade
    2. detect the text.
    3. return both the problem's name and its grade.
    example:
    a = detect_text(text_image)
    a = ["Three combination", "V8"]
    """
    return None


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
    path = "/Users/patrickdharma/Desktop/programming/openCV/moonboard_DatasetProject/Resources/Photos/moonboard.PNG"
    img, gray_blurred = read_image(path)
    board_part, text_part = crop_img(gray_blurred)
    detect_circle(board_part)
    
    # call the mouse_callback function with the cropped image part
    # mouse_callback("measurer", board_part)




