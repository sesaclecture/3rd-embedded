from src.main import (get_current_path_command, make_bootargs_command,
                      make_change_directory_command, make_list_command,
                      make_printenv_command)


def test_get_current_path_command():
    result = get_current_path_command()

    assert isinstance(result, str)
    assert len(result) > 0

    assert result == "pwd"


def test_make_list_command():
    normal = make_list_command(False)
    hidden = make_list_command(True)

    assert isinstance(normal, str)
    assert isinstance(hidden, str)

    assert normal == "ls"

    assert hidden.startswith("ls")
    assert "-" in hidden
    assert "a" in hidden
    assert "l" in hidden


def test_make_change_directory_command():
    paths = [
        "/boot",
        "/tmp",
        "/home/ubuntu",
        "/etc",
    ]

    for path in paths:
        result = make_change_directory_command(path)

        assert isinstance(result, str)
        assert result.startswith("cd ")
        assert result.endswith(path)
        assert "  " not in result


def test_make_printenv_command():
    env_names = [
        "bootargs",
        "baudrate",
        "kernel_addr_r",
        "ipaddr",
    ]

    for env_name in env_names:
        result = make_printenv_command(env_name)

        assert isinstance(result, str)
        assert result.startswith("printenv ")
        assert result.endswith(env_name)


def test_make_bootargs_command():
    result = make_bootargs_command(
        "ttyS0",
        "/dev/mmcblk0p2",
    )

    assert isinstance(result, str)
    assert result.startswith("setenv")
    assert "bootargs" in result
    assert "console=" in result
    assert "ttyS0" in result
    assert "root=" in result
    assert "/dev/mmcblk0p2" in result
    assert "rw" in result
    assert "  " not in result
