from src.main import (direction_to_twist, melody_to_frequencies,
                      note_to_frequency, servo_angle_to_pulse_width,
                      twist_to_wheel_speed)


def test_servo_angle_to_pulse_width():
    assert servo_angle_to_pulse_width(0) == 500
    assert servo_angle_to_pulse_width(90) == 1500
    assert servo_angle_to_pulse_width(180) == 2500

    result = servo_angle_to_pulse_width(45)

    assert isinstance(result, int)
    assert result == 1000


def test_note_to_frequency():
    assert note_to_frequency("C4") == 262
    assert note_to_frequency("D4") == 294
    assert note_to_frequency("E4") == 330
    assert note_to_frequency("F4") == 349
    assert note_to_frequency("G4") == 392
    assert note_to_frequency("A4") == 440
    assert note_to_frequency("B4") == 494
    assert note_to_frequency("C5") == 523

    assert note_to_frequency("UNKNOWN") == 0


def test_melody_to_frequencies():
    result = melody_to_frequencies(
        ["C4", "D4", "E4", "F4"]
    )

    assert isinstance(result, list)
    assert result == [262, 294, 330, 349]

    result = melody_to_frequencies(
        ["G4", "A4", "B4", "C5"]
    )

    assert result == [392, 440, 494, 523]


def test_direction_to_twist():
    assert direction_to_twist("forward") == (1.0, 0.0)
    assert direction_to_twist("backward") == (-1.0, 0.0)
    assert direction_to_twist("left") == (0.0, 1.0)
    assert direction_to_twist("right") == (0.0, -1.0)
    assert direction_to_twist("stop") == (0.0, 0.0)

    assert direction_to_twist("invalid") == (0.0, 0.0)


def test_twist_to_wheel_speed():
    assert twist_to_wheel_speed(1.0, 0.0) == (100, 100)
    assert twist_to_wheel_speed(0.5, 0.0) == (50, 50)

    assert twist_to_wheel_speed(0.5, 0.5) == (0, 100)
    assert twist_to_wheel_speed(0.5, -0.5) == (100, 0)

    assert twist_to_wheel_speed(2.0, 0.0) == (100, 100)
    assert twist_to_wheel_speed(-2.0, 0.0) == (-100, -100)
