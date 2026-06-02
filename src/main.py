# 문제 1.
#
# ROS2 Python Package 생성 명령어를 생성하세요.
#
# package_name은 생성할 패키지 이름입니다.
#
# 강의 시간에 사용한 ros2 pkg create 명령어를 활용하세요.
def make_ros2_pkg_create_command(package_name):
    return (
        f"ros2 pkg create "
        f"--build-type ament_python "
        f"{package_name}"
    )


# 문제 2.
#
# 특정 Topic 데이터를 확인하는 ROS2 명령어를 생성하세요.
#
# topic_name은 확인할 Topic 이름입니다.
#
# 강의 시간에 사용한 ros2 topic 명령어를 활용하세요.
def make_ros2_topic_echo_command(topic_name):
    return f"ros2 topic echo {topic_name}"


# 문제 3.
#
# 특정 Node를 실행하는 ROS2 명령어를 생성하세요.
#
# package_name은 패키지 이름입니다.
# node_name은 실행할 노드 이름입니다.
#
# 강의 시간에 사용한 ros2 run 명령어를 활용하세요.
def make_ros2_run_command(package_name, node_name):
    return f"ros2 run {package_name} {node_name}"


# 문제 4.
#
# Launch 파일을 실행하는 ROS2 명령어를 생성하세요.
#
# package_name은 패키지 이름입니다.
# launch_file은 launch 파일 이름입니다.
#
# 강의 시간에 사용한 ros2 launch 명령어를 활용하세요.
def make_ros2_launch_command(package_name, launch_file):
    return f"ros2 launch {package_name} {launch_file}"


# 문제 5.
#
# Raspberry Pi에서 ROS2 Docker Container를 실행하기 위한
# 명령어를 생성하세요.
#
# container_name은 컨테이너 이름입니다.
# image_name은 Docker 이미지 이름입니다.
#
# 아래 기능을 지원해야 합니다.
#
# - Detached Mode
# - Container Name 지정
# - Host Network 사용
# - X11 GUI Forwarding 지원
#
# 강의 시간에 사용한 docker run 명령어를 활용하세요.
def make_ros2_docker_run_command(
    container_name,
    image_name,
):
    return (
        f"docker run -dit "
        f"--name {container_name} "
        f"--network host "
        f"-e DISPLAY=:0 "
        f"-v /tmp/.X11-unix:/tmp/.X11-unix "
        f"{image_name}"
    )
