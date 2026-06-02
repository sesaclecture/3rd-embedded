from src.main import (make_scp_upload_command, make_ssh_command,
                      make_ssh_keygen_command, make_ssh_target,
                      make_x11_ssh_command)


def test_make_ssh_target():
    result = make_ssh_target(
        "pi",
        "192.168.0.10",
    )

    assert isinstance(result, str)

    assert "pi" in result
    assert "192.168.0.10" in result
    assert "@" in result

    assert " " not in result


def test_make_ssh_command():
    result = make_ssh_command(
        "pi",
        "192.168.0.10",
    )

    assert isinstance(result, str)

    assert result.startswith("ssh ")

    assert "pi@192.168.0.10" in result

    assert "scp" not in result
    assert "sftp" not in result


def test_make_ssh_keygen_command():
    result = make_ssh_keygen_command(
        "~/.ssh/id_ed25519",
    )

    assert isinstance(result, str)

    assert result.startswith("ssh-keygen")

    assert "-t" in result
    assert "ed25519" in result

    assert "-f" in result

    assert "~/.ssh/id_ed25519" in result


def test_make_scp_upload_command():
    result = make_scp_upload_command(
        "./hello.py",
        "pi",
        "192.168.0.10",
        "/home/pi/hello.py",
    )

    assert isinstance(result, str)

    assert result.startswith("scp ")

    assert "./hello.py" in result

    assert "pi@192.168.0.10" in result

    assert ":/home/pi/hello.py" in result


def test_make_x11_ssh_command():
    result = make_x11_ssh_command(
        "pi",
        "192.168.0.10",
    )

    assert isinstance(result, str)

    assert result.startswith("ssh ")
    assert "pi@192.168.0.10" in result

    assert "-CY" in result or "-YC" in result
