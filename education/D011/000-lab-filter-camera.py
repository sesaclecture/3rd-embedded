import cv2
import numpy as np


def nothing(x): pass
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 800, 260)
cv2.createTrackbar("L Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("A Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("A Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("B Min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("B Max", "Trackbars", 255, 255, nothing)

cap = cv2.VideoCapture(4)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    l_min = cv2.getTrackbarPos("L Min", "Trackbars")
    l_max = cv2.getTrackbarPos("L Max", "Trackbars")
    a_min = cv2.getTrackbarPos("A Min", "Trackbars")
    a_max = cv2.getTrackbarPos("A Max", "Trackbars")
    b_min = cv2.getTrackbarPos("B Min", "Trackbars")
    b_max = cv2.getTrackbarPos("B Max", "Trackbars")

    lower = np.array([l_min, a_min, b_min])
    upper = np.array([l_max, a_max, b_max])
    mask = cv2.inRange(lab, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    combined = np.hstack((frame, result))
    cv2.imshow("LAB Filter Result ", cv2.resize(combined, (1280, 600)))

    key = cv2.waitKey(33)
    if key == 27: # ESE to exit
        break

cap.release()
cv2.destroyAllWindows()
