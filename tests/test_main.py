import cv2
import numpy as np
from src.main import (calculate_channel_mean, convert_to_hsv, convert_to_lab,
                      count_mask_pixels, create_color_mask)


def test_convert_to_hsv():
    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    hsv = convert_to_hsv(image)

    assert isinstance(
        hsv,
        np.ndarray,
    )

    assert hsv.shape == image.shape


def test_convert_to_lab():
    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    lab = convert_to_lab(image)

    assert isinstance(
        lab,
        np.ndarray,
    )

    assert lab.shape == image.shape


def test_calculate_channel_mean():
    image = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    image[:, :, 2] = 100

    mean_value = calculate_channel_mean(
        image,
        2,
    )

    assert mean_value == 100.0


def test_create_color_mask():
    hsv = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    hsv[0:5, 0:5] = [
        100,
        150,
        150,
    ]

    lower = np.array(
        [90, 100, 100]
    )

    upper = np.array(
        [110, 255, 255]
    )

    mask = create_color_mask(
        hsv,
        lower,
        upper,
    )

    assert mask.shape == (
        10,
        10,
    )

    assert mask[0, 0] == 255

    assert mask[8, 8] == 0


def test_count_mask_pixels():
    mask = np.zeros(
        (10, 10),
        dtype=np.uint8,
    )

    mask[0:5, 0:5] = 255

    count = count_mask_pixels(
        mask
    )

    assert count == 25
