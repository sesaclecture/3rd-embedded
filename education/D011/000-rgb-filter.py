import cv2
import numpy as np


def nothing(x): pass
# Trackbar UI
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 800, 260)
cv2.createTrackbar("R Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("G Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("B Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("B Max", "Trackbars", 255, 255, nothing)

img = cv2.imread("fruit.jpg") # image file load
while True:
    # Trackbar values
    r_min = cv2.getTrackbarPos("R Min", "Trackbars")
    r_max = cv2.getTrackbarPos("R Max", "Trackbars")
    g_min = cv2.getTrackbarPos("G Min", "Trackbars")
    g_max = cv2.getTrackbarPos("G Max", "Trackbars")
    b_min = cv2.getTrackbarPos("B Min", "Trackbars")
    b_max = cv2.getTrackbarPos("B Max", "Trackbars")
    # Filter in BGR space (OpenCV uses BGR)
    lower = np.array([b_min, g_min, r_min])
    upper = np.array([b_max, g_max, r_max])
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    # Show filtered result
    combined = np.hstack((img, result))
    cv2.imshow("RGB Filter Result", cv2.resize(combined, (1280, 600)))
    key = cv2.waitKey(33)
    if key == 27: # 'ESC' to exit
        break

cv2.destroyAllWindows()
