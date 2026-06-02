import cv2
import numpy as np


# 문제 1.
#
# BGR 이미지를 Gray 이미지로 변환하세요.
#
# OpenCV 함수를 활용하세요.
def convert_to_gray(image):
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )


# 문제 2.
#
# 이미지를 지정한 크기로 변경하세요.
#
# width와 height를 사용하여
# 새로운 크기의 이미지를 반환해야 합니다.
def resize_image(
    image,
    width,
    height,
):
    return cv2.resize(
        image,
        (width, height),
    )


# 문제 3.
#
# Gray 이미지에 Binary Threshold를 적용하세요.
#
# threshold_value를 기준으로
# Binary 이미지를 생성해야 합니다.
#
# 반환값은 Binary Image 입니다.
def apply_threshold(
    gray_image,
    threshold_value,
):
    _, binary = cv2.threshold(
        gray_image,
        threshold_value,
        255,
        cv2.THRESH_BINARY,
    )

    return binary


# 문제 4.
#
# 이미지에서 빨간색 픽셀 개수를 계산하세요.
#
# BGR 이미지를 입력으로 받습니다.
#
# 빨간색 조건:
# R > 200
# G < 50
# B < 50
#
# 조건에 맞는 픽셀 개수를 반환하세요.
def count_red_pixels(image):
    blue = image[:, :, 0]
    green = image[:, :, 1]
    red = image[:, :, 2]

    mask = (
        (red > 200)
        & (green < 50)
        & (blue < 50)
    )

    return int(np.sum(mask))


# 문제 5.
#
# Binary Mask에서 객체 중심 좌표를 계산하세요.
#
# 흰색 픽셀(255)의 평균 위치를 이용하여
# 중심 좌표를 계산합니다.
#
# 반환값:
# (cx, cy)
#
# 객체가 없으면 None 반환
def find_object_center(mask):
    ys, xs = np.where(mask == 255)

    if len(xs) == 0:
        return None

    cx = int(np.mean(xs))
    cy = int(np.mean(ys))

    return (cx, cy)
