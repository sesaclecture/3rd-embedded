from src.main import (make_ros2_docker_run_command, make_ros2_launch_command,
                      make_ros2_pkg_create_command, make_ros2_run_command,
                      make_ros2_topic_echo_command)


def test_make_ros2_pkg_create_command():
    result = make_ros2_pkg_create_command(
        "my_robot_pkg"
    )

    assert isinstance(result, str)

    assert result.startswith("ros2")

    assert "pkg" in result
    assert "create" in result

    assert "ament_python" in result

    assert "my_robot_pkg" in result


def test_make_ros2_topic_echo_command():
    result = make_ros2_topic_echo_command(
        "/chatter"
    )

    assert isinstance(result, str)

    assert result.startswith("ros2")

    assert "topic" in result
    assert "echo" in result

    assert "/chatter" in result


def test_make_ros2_run_command():
    result = make_ros2_run_command(
        "my_pkg",
        "publisher",
    )

    assert isinstance(result, str)

    assert result.startswith("ros2")

    assert "run" in result

    assert "my_pkg" in result
    assert "publisher" in result


def test_make_ros2_launch_command():
    result = make_ros2_launch_command(
        "my_pkg",
        "robot.launch.py",
    )

    assert isinstance(result, str)

    assert result.startswith("ros2")

    assert "launch" in result

    assert "my_pkg" in result
    assert "robot.launch.py" in result


def test_make_ros2_docker_run_command():
    result = make_ros2_docker_run_command(
        "ros2_pi",
        "ros:humble",
    )

    assert isinstance(result, str)

    assert result.startswith("docker run")

    assert "-dit" in result

    assert "--name" in result
    assert "ros2_pi" in result

    assert "--network host" in result

    assert "DISPLAY" in result

    assert "/tmp/.X11-unix" in result

    assert "ros:humble" in result
