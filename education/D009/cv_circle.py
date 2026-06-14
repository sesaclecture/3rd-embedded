import cv2

# 클릭한 좌표들을 저장
points = []


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"clicked: x={x}, y={y}")
        points.append((x, y))


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("camera open failed")
    exit(1)

cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", draw_circle)

while True:
    ret, frame = cap.read()
    if not ret:
        print("frame read failed")
        break

    # 저장된 클릭 좌표를 매 프레임마다 다시 그림
    for x, y in points:
        cv2.circle(frame, (x, y), 20, (255, 0, 0), -1)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    # c 누르면 그린 원 초기화
    if key == ord("c"):
        points.clear()

cap.release()
cv2.destroyAllWindows()
