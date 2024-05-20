import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Load the image
img = cv.imread("../Resources/Photos/moonboard.PNG")
if img is None:
    print("Failed to load image.")
    exit()
# convert the image to hsv
hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Define the lower and upper bounds of the two segments of red
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])

# Create masks for both ranges and combine
mask1 = cv.inRange(hsv_img, lower_red1, upper_red1)
mask2 = cv.inRange(hsv_img, lower_red2, upper_red2)
mask = cv.bitwise_or(mask1, mask2)

# Apply the mask to the original image
result = cv.bitwise_and(img, img, mask=mask)
result_centers = img.copy()  # Corrected: use copy() to actually copy the image

# Find contours in the mask
contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Draw contours and find the centers
for contour in contours:
    M = cv.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv.circle(result_centers, (cx, cy), 5, (255, 0, 0), -1)  # Draw a blue circle at the center
        print(f"Center coordinates: x:{cx} y:{cy}")

# Convert result to RGB for plotting
result_rgb = cv.cvtColor(result_centers, cv.COLOR_BGR2RGB)
