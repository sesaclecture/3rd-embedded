import os

import cv2

# 동영상 파일 열기
cap = cv2.VideoCapture("ronaldinho.mp4")

# fps 가져오기 (없으면 기본값 30 사용)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30
delay = int(1000 / fps)

# 저장용 카운터
save_count = 1

while True:
    ret, frame = cap.read()

    if not ret:
        # 영상이 끝났으면 처음부터 다시 재생
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # 크기를 절반으로 줄이기
    h, w = frame.shape[:2]
    frame = cv2.resize(frame, (w // 2, h // 2))

    # 화면 출력
    cv2.imshow("Frame", frame)

    # 키 입력 처리
    key = cv2.waitKey(delay) & 0xFF

    if key == ord('q'):   # 종료
        break
    elif key == ord('c'): # 현재 프레임 저장
        filename = f"{save_count:03d}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        save_count += 1

cap.release()
cv2.destroyAllWindows()
