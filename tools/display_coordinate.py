import cv2

# Function to display the coordinates of the points where mouse is clicked
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left button of the mouse is clicked
        print(f"x:{x}, y:{y}")  # Print the coordinates of the point clicked

# Load the image
img = cv2.imread('../Resources/Photos/V3/V3_1.PNG')

# Create a window and set a mouse callback function that calls `click_event`
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_event)

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
