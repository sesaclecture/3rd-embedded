from src.main import (make_compose_service, make_docker_pull_command,
                      make_docker_run_command, make_port_mapping_command,
                      make_volume_mapping_command)


def test_make_docker_pull_command():
    result = make_docker_pull_command("ubuntu")

    assert isinstance(result, str)

    assert result.startswith("docker")
    assert "pull" in result
    assert "ubuntu" in result


def test_make_docker_run_command():
    result = make_docker_run_command("nginx")

    assert isinstance(result, str)

    assert result.startswith("docker")
    assert "run" in result
    assert "nginx" in result


def test_make_port_mapping_command():
    result = make_port_mapping_command(
        "nginx",
        8080,
        80,
    )

    assert isinstance(result, str)

    assert "docker run" in result
    assert "-p" in result

    assert "8080:80" in result

    assert "nginx" in result


def test_make_volume_mapping_command():
    result = make_volume_mapping_command(
        "/home/pi/data",
        "/data",
        "ubuntu",
    )

    assert isinstance(result, str)

    assert "docker run" in result

    assert "-v" in result

    assert "/home/pi/data:/data" in result

    assert "ubuntu" in result


def test_make_compose_service():
    result = make_compose_service(
        "web",
        "nginx",
        8080,
        80,
    )

    assert isinstance(result, str)

    assert "web:" in result

    assert "image:" in result
    assert "nginx" in result

    assert "ports:" in result

    assert "8080:80" in result
