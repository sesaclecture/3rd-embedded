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

# 기본값 생성
cfg = {k: v for k, v in keys}

# 기존 파일에서 값 불러오기
if os.path.exists(json_name):
    try:
        with open(json_name, "r") as f:
            loaded_cfg = json.load(f)

        # 기존 JSON에 일부 key가 빠져 있어도 기본값 유지
        cfg.update(loaded_cfg)

        print(f"Loaded calibration file: {json_name}")

    except json.JSONDecodeError:
        print(f"[WARN] Invalid JSON file: {json_name}")
        print("[WARN] Using default LAB values")

    except Exception as e:
        print(f"[WARN] Failed to load {json_name}: {e}")
        print("[WARN] Using default LAB values")
else:
    print(f"[INFO] {json_name} not found. Using default LAB values")


cv2.namedWindow("Trackbars")

for k, v in keys:
    init_value = int(cfg.get(k, v))
    init_value = max(0, min(255, init_value))
    cv2.createTrackbar(k, "Trackbars", init_value, 255, nothing)


cap = cv2.VideoCapture(4)

if not cap.isOpened():
    print("[ERROR] Failed to open camera")
    exit(1)


while True:
    ret, frame = cap.read()

    if not ret:
        print("[ERROR] Failed to read camera frame")
        break

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    vals = [cv2.getTrackbarPos(k, "Trackbars") for k, _ in keys]

    lower = np.array(vals[::2], dtype=np.uint8)
    upper = np.array(vals[1::2], dtype=np.uint8)

    mask = cv2.inRange(lab, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Original", cv2.resize(frame, (640, 480)))
    cv2.imshow("LAB Mask", cv2.resize(mask, (640, 480)))
    cv2.imshow("LAB Filter", cv2.resize(res, (640, 480)))

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

    elif key == 27 or key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
