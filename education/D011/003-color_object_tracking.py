import json
import os
from datetime import datetime

import cv2
import numpy as np


def nothing(x):
    pass


json_name = "LAB-cal.json"

keys = [
    ("l_min", 0),
    ("l_max", 255),
    ("a_min", 0),
    ("a_max", 255),
    ("b_min", 0),
    ("b_max", 255),
]

# 기본값 준비
cfg = {k: v for k, v in keys}

# 기존 파일에서 값 불러오기
if os.path.exists(json_name):
    with open(json_name, "r") as f:
        loaded_cfg = json.load(f)
        cfg.update(loaded_cfg)
    print(f"Loaded {json_name}")
else:
    print(f"{json_name} not found. Use default values.")


cv2.namedWindow("Trackbars")

for k, v in keys:
    cv2.createTrackbar(k, "Trackbars", cfg.get(k, v), 255, nothing)


cap = cv2.VideoCapture(4)

if not cap.isOpened():
    print("Failed to open camera")
    exit(1)


while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    vals = [cv2.getTrackbarPos(k, "Trackbars") for k, _ in keys]

    lower, upper = np.array(vals[::2]), np.array(vals[1::2])
    mask = cv2.inRange(lab, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # 컨투어(윤곽선)들을 찾아서 contours 에 저장
    # OpenCV에서 객체 검출, 분할, 모양 분석, 측정 등에 가장 널리 사용됨
    # contours, hierarchy = cv2.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
    # method: 윤곽선 근사화(압축) 방법
    #   - cv2.CHAIN_APPROX_SIMPLE: 꼭짓점만 반환(메모리 절약)
    #   - cv2.CHAIN_APPROX_NONE: 모든 경계점 반환
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        # 각 컨투어의 면적 계산 후, 가장 큰 것 선택
        biggest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(biggest)  # (x, y): 좌상단, (w, h): 폭, 높이

        # 원본 이미지에 사각형 그리기
        cv2.rectangle(
            res,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # 사각형 좌표 표시
        cv2.putText(
            res,
            f"Rect: ({x},{y},{w},{h})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("LAB Filter", cv2.resize(res, (640, 480)))
    cv2.imshow("Mask", cv2.resize(mask, (640, 480)))

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        out = dict(zip([k for k, _ in keys], vals))

        now = datetime.now().strftime("%y%m%d-%H%M%S")

        with open(f"LAB-cal-{now}.json", "w") as f:
            json.dump(out, f, indent=4)

        with open(json_name, "w") as f:
            json.dump(out, f, indent=4)

        print(f"Saved LAB-cal-{now}.json & {json_name}")
        print(out)

    elif key == 27:
        break


cap.release()
cv2.destroyAllWindows()
