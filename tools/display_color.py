from matplotlib.colors import hsv_to_rgb
import numpy as np
import matplotlib.pyplot as plt
"""
A simple way to display the colors in Python is to make small square images 
of the desired color and plot them in Matplotlib. Matplotlib only interprets colors 
in RGB, but handy conversion functions are provided for the major color spaces so 
that we can plot images in other color spaces:
"""
# lower red range
lower = np.array([0, 100, 100])
upper = np.array([10, 255, 255])

# Upper red range
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

left_square = np.full((10, 10, 3), lower_red2, dtype=np.uint8) / 255.0
right_square = np.full((10, 10, 3), upper_red2, dtype=np.uint8) / 255.0

# plot them together by converting them to RGB for viewing

plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(left_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(right_square))
plt.show()
