import cv2 as cv


# basics Resizing & Rescaling
# used to prevent computational strain, as large media files tend to store a lot of info in it.
def rescaleFrame(frame, scale=0.75):
    # work for Images, Videos, and Live Video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)

# change resolution function
def changeRes(width, height):
    # works only for Live video
    capture.set(3, width)  # 3 references the width
    capture.set(4, height)  # 4 references the height

# reading image
img = cv.imread("../Resources/Photos/cat.jpg")  # show image
cv.imshow("cat", img)

resized_image = rescaleFrame(img)  # resize image
cv.imshow('Image', resized_image)


# reading videos
capture = cv.VideoCapture("../Resources/Videos/dog.mp4")

while True:
    isTrue, frame = capture.read()

    frame_resized = rescaleFrame(frame)

    cv.imshow('Video', frame)
    cv.imshow('Video resized', frame_resized)  # resizing image

    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()


