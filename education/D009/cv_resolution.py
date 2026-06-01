import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Linux면 CAP_V4L2가 안정적
candidates = [
    (1920,1080), (1280,720), (1024,576), (960,540),
    (800,600), (800,450), (720,480), (640,480), (640,360), (320,240)
]

ok_modes = []
for (w,h) in candidates:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    aw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    ah = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (aw,ah) == (w,h):
        ok_modes.append((w,h))

print("지원/적용 확인된 해상도:", ok_modes if ok_modes else "없음(드라이버/포맷 제한 가능)")
cap.release()
