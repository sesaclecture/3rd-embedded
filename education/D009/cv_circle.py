import cv2

# 전역 변수로 사용할 프레임
frame = None

# 마우스 이벤트 콜백 함수
def draw_circle(event, x, y, flags, param):
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭
        cv2.circle(frame, (x, y), 20, (255, 0, 0), -1)
        # (x,y) 중심에 반지름 20, 파란색 원을 채워서 그림

# 카메라 열기
cap = cv2.VideoCapture(0)

# 창 생성 및 마우스 콜백 등록
cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", draw_circle)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Camera", frame)

    # 'q' 입력 시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
