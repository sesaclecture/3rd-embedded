import cv2

img = cv2.imread('tux.jpg')
cropped = img[20:270, 320:520]
resized = cv2.resize(cropped, (400, 200))

cv2.imshow("Original", img)
cv2.imshow("Cropped image", cropped)
cv2.imshow("Resized image", resized)

width, height, channels = img.shape
print(f"Width: {width}, Height: {height}, Channels: {channels}")
resize = cv2.resize(img, (int(width * 1.5), int(height * 1.5)))
cv2.imwrite("tux2.jpg", resize)

rotated = cv2.rotate(resize, cv2.ROTATE_90_CLOCKWISE)
cv2.imshow("Rotated image", rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()
