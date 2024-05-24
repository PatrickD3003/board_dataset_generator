import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# ROI (Region Of Interest)
# ROI[top:bottom, left:right]を使って画像データを切り出す
def crop_img(img):
    # Ensure indices are within the image size: [row_start:row_end, col_start:col_end]
    board_part = img[600:2332, 26:1124]  # Check if these indices are correct given your image's width is only 1170
    text_part = img[328:514, 291:889]
    return board_part, text_part

# Load the image
img = cv.imread("../Resources/Photos/moonboard.PNG")

# Check dimensions of the image
print("Original image dimensions:", img.shape)

# Obtain ROI parts
board_part, text_part = crop_img(img)

# Display the ROIs
cv.imshow("board part", board_part)
cv.imshow("text part", text_part)
cv.waitKey(0)
cv.destroyAllWindows()
