import json

import cv2
import numpy as np


# 문제 1.
#
# OpenCV 색상 필터 설정을 저장하기 위한 dict를 생성하세요.
#
# color_space는 색상 공간 이름입니다.
# lower는 필터 하한값 리스트입니다.
# upper는 필터 상한값 리스트입니다.
#
# 반환값에는 아래 key가 포함되어야 합니다.
#
# - color_space
# - lower
# - upper
def make_filter_config(
    color_space,
    lower,
    upper,
):
    return {
        "color_space": color_space,
        "lower": lower,
        "upper": upper,
    }


# 문제 2.
#
# JSON 문자열에서 필터 설정값을 불러오세요.
#
# json_text는 필터 설정이 저장된 JSON 문자열입니다.
#
# 반환값은 아래 순서의 튜플입니다.
#
# (color_space, lower, upper)
def load_filter_config(json_text):
    config = json.loads(json_text)

    return (
        config["color_space"],
        config["lower"],
        config["upper"],
    )


# 문제 3.
#
# Binary Mask에서 객체의 Bounding Box를 찾으세요.
#
# 흰색 픽셀 값은 255입니다.
#
# 반환값은 아래 순서의 튜플입니다.
#
# (x, y, w, h)
#
# 객체가 없으면 None을 반환하세요.
def find_bounding_box(mask):
    ys, xs = np.where(mask == 255)

    if len(xs) == 0:
        return None

    x_min = int(np.min(xs))
    x_max = int(np.max(xs))

    y_min = int(np.min(ys))
    y_max = int(np.max(ys))

    w = x_max - x_min + 1
    h = y_max - y_min + 1

    return (
        x_min,
        y_min,
        w,
        h,
    )


# 문제 4.
#
# 객체의 중심 위치와 크기를 기준으로
# 로봇 추적 명령을 결정하세요.
#
# center_x는 객체 중심의 x 좌표입니다.
# image_width는 이미지 전체 너비입니다.
# object_area는 객체 영역의 크기입니다.
#
# 반환해야 하는 명령은 아래 중 하나입니다.
#
# - turn_left
# - turn_right
# - forward
# - stop
def decide_tracking_command(
    center_x,
    image_width,
    object_area,
):
    left_boundary = image_width * 0.4
    right_boundary = image_width * 0.6

    stop_area = 5000

    if center_x < left_boundary:
        return "turn_left"

    if center_x > right_boundary:
        return "turn_right"

    if object_area >= stop_area:
        return "stop"

    return "forward"


# 문제 5.
#
# 추적 명령을 ROS2 Twist 제어값으로 변환하세요.
#
# 반환값은 아래 순서의 튜플입니다.
#
# (linear_x, angular_z)
def command_to_twist(command):
    twist_table = {
        "forward": (0.2, 0.0),
        "turn_left": (0.0, 0.5),
        "turn_right": (0.0, -0.5),
        "stop": (0.0, 0.0),
    }

    return twist_table.get(command, (0.0, 0.0))
