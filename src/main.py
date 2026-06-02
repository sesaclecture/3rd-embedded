import cv2
import numpy as np


# 문제 1.
#
# BGR 이미지를 HSV 이미지로 변환하세요.
#
# OpenCV 함수를 활용하세요.
def convert_to_hsv(image):
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV,
    )


# 문제 2.
#
# BGR 이미지를 LAB 이미지로 변환하세요.
#
# OpenCV 함수를 활용하세요.
def convert_to_lab(image):
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB,
    )


# 문제 3.
#
# 지정한 채널의 평균값을 계산하세요.
#
# channel_index는 사용할 채널 번호입니다.
def calculate_channel_mean(
    image,
    channel_index,
):
    return float(
        np.mean(
            image[:, :, channel_index]
        )
    )


# 문제 4.
#
# Color Mask를 생성하세요.
#
# image는 HSV 또는 LAB 이미지입니다.
#
# lower와 upper는 각각
# 색상 범위의 하한과 상한입니다.
#
# OpenCV 함수를 활용하세요.
def create_color_mask(
    image,
    lower,
    upper,
):
    return cv2.inRange(
        image,
        lower,
        upper,
    )


# 문제 5.
#
# Binary Mask에서 활성 픽셀 개수를 계산하세요.
#
# 활성 픽셀은 값이 255인 픽셀입니다.
#
# 반환값은 픽셀 개수입니다.
def count_mask_pixels(mask):
    return int(
        np.sum(mask == 255)
    )
