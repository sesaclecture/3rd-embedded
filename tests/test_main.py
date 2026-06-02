import json

import numpy as np
from src.main import (command_to_twist, decide_tracking_command,
                      find_bounding_box, load_filter_config,
                      make_filter_config)


def test_make_filter_config():
    config = make_filter_config(
        "HSV",
        [0, 100, 100],
        [10, 255, 255],
    )

    assert isinstance(config, dict)

    assert config["color_space"] == "HSV"
    assert config["lower"] == [0, 100, 100]
    assert config["upper"] == [10, 255, 255]


def test_load_filter_config():
    json_text = json.dumps(
        {
            "color_space": "LAB",
            "lower": [20, 130, 120],
            "upper": [255, 180, 170],
        }
    )

    color_space, lower, upper = load_filter_config(
        json_text
    )

    assert color_space == "LAB"
    assert lower == [20, 130, 120]
    assert upper == [255, 180, 170]


def test_find_bounding_box():
    mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    mask[20:50, 30:70] = 255

    box = find_bounding_box(mask)

    assert box == (30, 20, 40, 30)

    empty_mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    assert find_bounding_box(empty_mask) is None


def test_decide_tracking_command():
    assert decide_tracking_command(
        100,
        640,
        1000,
    ) == "turn_left"

    assert decide_tracking_command(
        540,
        640,
        1000,
    ) == "turn_right"

    assert decide_tracking_command(
        320,
        640,
        1000,
    ) == "forward"

    assert decide_tracking_command(
        320,
        640,
        6000,
    ) == "stop"


def test_command_to_twist():
    assert command_to_twist("forward") == (0.2, 0.0)
    assert command_to_twist("turn_left") == (0.0, 0.5)
    assert command_to_twist("turn_right") == (0.0, -0.5)
    assert command_to_twist("stop") == (0.0, 0.0)

    assert command_to_twist("invalid") == (0.0, 0.0)
