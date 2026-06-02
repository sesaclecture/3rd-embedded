# 문제 1.
#
# 현재 작업 디렉토리를 확인하는 Linux 명령어를 반환하세요.
#
# 강의 시간에 실습한 Linux 명령어를 활용하세요.
def get_current_path_command():
    return "pwd"


# 문제 2.
#
# 파일 목록을 조회하는 Linux 명령어를 생성하세요.
#
# hidden 값에 따라 동작이 달라져야 합니다.
#
# hidden=True
#   숨김 파일을 포함하여 자세히 출력
#
# hidden=False
#   일반 파일 목록 출력
#
# 강의 시간에 사용한 옵션을 활용하세요.
def make_list_command(hidden):
    if hidden:
        return "ls -al"

    return "ls"


# 문제 3.
#
# 전달받은 경로로 이동하기 위한 Linux 명령어를 생성하세요.
#
# path 인자는 이동할 디렉토리 경로입니다.
def make_change_directory_command(path):
    return f"cd {path}"


# 문제 4.
#
# U-Boot 환경변수를 조회하는 명령어를 생성하세요.
#
# env_name 인자는 조회할 환경변수 이름입니다.
#
# 강의 중 확인한 U-Boot 명령어를 활용하세요.
def make_printenv_command(env_name):
    return f"printenv {env_name}"


# 문제 5.
#
# U-Boot bootargs 환경변수를 설정하는 명령어를 생성하세요.
#
# console 인자는 시리얼 콘솔 장치 이름입니다.
# rootfs 인자는 루트 파일시스템 장치 이름입니다.
#
# 생성되는 명령어에는 아래 정보가 포함되어야 합니다.
#
# - console
# - root
# - rw
#
# 강의 중 실습한 bootargs 형식을 참고하세요.
def make_bootargs_command(console, rootfs):
    return (
        f"setenv bootargs "
        f"console={console},115200 "
        f"root={rootfs} "
        f"rw"
    )
