import cv2
import numpy as np
from src.main import (apply_threshold, convert_to_gray, count_red_pixels,
                      find_object_center, resize_image)


def test_convert_to_gray():
    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    gray = convert_to_gray(image)

    assert len(gray.shape) == 2

    assert gray.shape == (100, 100)


def test_resize_image():
    image = np.zeros(
        (100, 200, 3),
        dtype=np.uint8,
    )

    resized = resize_image(
        image,
        50,
        25,
    )

    assert resized.shape[0] == 25
    assert resized.shape[1] == 50


def test_apply_threshold():
    gray = np.array(
        [
            [50, 150],
            [200, 20],
        ],
        dtype=np.uint8,
    )

    binary = apply_threshold(
        gray,
        100,
    )

    assert binary[0, 0] == 0
    assert binary[0, 1] == 255

    assert binary[1, 0] == 255
    assert binary[1, 1] == 0


def test_count_red_pixels():
    image = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    image[0:5, 0:5] = [0, 0, 255]

    count = count_red_pixels(image)

    assert count == 25


def test_find_object_center():
    mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    mask[40:60, 20:40] = 255

    center = find_object_center(mask)

    assert center == (29, 49)

    empty_mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    assert (
        find_object_center(
            empty_mask
        )
        is None
    )
