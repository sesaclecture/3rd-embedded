# 문제 1.
#
# SSH 접속 대상 문자열을 생성하세요.
#
# user 인자는 접속할 사용자 이름입니다.
# host 인자는 접속할 장비의 IP 주소 또는 호스트 이름입니다.
#
# SSH, SCP, SFTP 명령어에서 공통으로 사용하는
# 접속 대상 형식을 반환해야 합니다.
def make_ssh_target(user, host):
    return f"{user}@{host}"


# 문제 2.
#
# SSH 접속 명령어를 생성하세요.
#
# user와 host 정보를 이용하여
# 원격 장비에 터미널로 접속하기 위한 명령어를 반환해야 합니다.
def make_ssh_command(user, host):
    return f"ssh {make_ssh_target(user, host)}"


# 문제 3.
#
# SSH Key 생성 명령어를 생성하세요.
#
# key_path 인자는 생성할 SSH private key 파일 경로입니다.
#
# 비밀번호 없는 SSH 접속을 준비하기 위한
# keygen 명령어를 반환해야 합니다.
def make_ssh_keygen_command(key_path):
    return f"ssh-keygen -t ed25519 -f {key_path}"


# 문제 4.
#
# SCP 업로드 명령어를 생성하세요.
#
# local_path 인자는 호스트 PC에 있는 파일 경로입니다.
# user와 host는 원격 장비 접속 정보입니다.
# remote_path 인자는 원격 장비에 저장할 파일 경로입니다.
#
# 호스트 PC의 파일을 원격 장비로 복사하는 명령어를 반환해야 합니다.
def make_scp_upload_command(local_path, user, host, remote_path):
    target = make_ssh_target(user, host)
    return f"scp {local_path} {target}:{remote_path}"


# 문제 5.
#
# X11 Forwarding이 포함된 SSH 접속 명령어를 생성하세요.
#
# user와 host 정보를 이용하여
# 원격 장비의 GUI 프로그램을 호스트 PC 화면에 띄울 수 있는
# SSH 명령어를 반환해야 합니다.
#
# 강의 시간에 사용한 SSH 압축 및
# Trusted X11 Forwarding 옵션을 포함하세요.
def make_x11_ssh_command(user, host):
    return f"ssh -CY {make_ssh_target(user, host)}"
