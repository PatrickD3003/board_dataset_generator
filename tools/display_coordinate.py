import cv2

# Function to display the coordinates of the points where mouse is clicked
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left button of the mouse is clicked
        print(x, ',', y)  # Print the coordinates of the point clicked

# Load the image
img = cv2.imread('/Users/wybeeboi/Documents/moonboard generator 2 /board_dataset_generator/Resources/Photos/A18.PNG')

# Create a window and set a mouse callback function that calls `click_event`
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_event)

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
