import cv2
import numpy as np

ORIGINAL_WINDOW = "Original Image"
HSV_WINDOW = "HSV Modified Image"

INPUT_PATH = "lena.png"

def nothing(x):
    pass


orig_img = cv2.imread(INPUT_PATH)

if orig_img is None:
    print(f"이미지를 불러올 수 없습니다: {INPUT_PATH}")
    exit(1)


cv2.namedWindow(ORIGINAL_WINDOW)
cv2.namedWindow(HSV_WINDOW)

cv2.createTrackbar("Hue", HSV_WINDOW, 0, 178, nothing)
cv2.createTrackbar("Saturation", HSV_WINDOW, 125, 250, nothing)
cv2.createTrackbar("Value", HSV_WINDOW, 125, 250, nothing)

while True:
    hue = cv2.getTrackbarPos("Hue", HSV_WINDOW)
    saturation = cv2.getTrackbarPos("Saturation", HSV_WINDOW)
    value = cv2.getTrackbarPos("Value", HSV_WINDOW)

    hsv_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_img)

    h_new = (h.astype(np.int16) + hue) % 179

    s_new = np.clip(
        s.astype(np.int16) + (saturation - 125),
        0,
        255
    )

    v_new = np.clip(
        v.astype(np.int16) + (value - 125),
        0,
        255
    )

    hsv_modified = cv2.merge([
        h_new.astype(np.uint8),
        s_new.astype(np.uint8),
        v_new.astype(np.uint8)
    ])

    modified_img = cv2.cvtColor(hsv_modified, cv2.COLOR_HSV2BGR)

    cv2.imshow(ORIGINAL_WINDOW, orig_img)
    cv2.imshow(HSV_WINDOW, modified_img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

cv2.destroyAllWindows()
