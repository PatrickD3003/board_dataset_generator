import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

moonboard = cv.imread("../Resources/Photos/moonboard.PNG")
# place each pixel in its location based on its components and color it by its color
# set up the plot
r, g, b = cv.split(moonboard)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

# set up the pixel colors
"""
reshaping and normalization required, 
you need the colors corresponding to every pixel in the image to be 
flattened into a list and normalized, so that they can be passed to the 
facecolors parameter of matplotlib scatter()

Normalizing->condensing the range of colors from 0-255 to 0-1 as required
for the facecolors parameter
*facecolors wants a list, not a NumPy array
"""

pixel_colors = moonboard.reshape((np.shape(moonboard)[0]*np.shape(moonboard)[1], 3))
norm = colors.Normalize(vmin=-1., vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()

"""
Now we have all the components ready for plotting: the pixel positions 
for each axis and their corresponding colors, in the format facecolors expects.
 You can build the scatter plot and view it:
"""
axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Red")
axis.set_ylabel("Green")
axis.set_zlabel("Blue")
plt.show()

