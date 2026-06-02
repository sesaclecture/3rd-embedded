# 문제 1.
#
# GPIO 입력 레벨을 상태 문자열로 변환하세요.
#
# level 값은 0 또는 1입니다.
# 0이면 "LOW", 1이면 "HIGH"를 반환해야 합니다.
def gpio_level_to_state(level):
    if level == 0:
        return "LOW"

    if level == 1:
        return "HIGH"

    return "UNKNOWN"


# 문제 2.
#
# UART 송신용 패킷을 생성하세요.
#
# message는 문자열입니다.
# 송신 데이터는 bytes 타입이어야 합니다.
# UART 메시지 끝에는 newline 문자가 포함되어야 합니다.
def make_uart_tx_packet(message):
    return f"{message}\n".encode("utf-8")


# 문제 3.
#
# UART 수신 패킷을 파싱하세요.
#
# packet은 bytes 타입입니다.
# 수신 데이터 끝의 newline 문자를 제거하고 문자열로 반환해야 합니다.
def parse_uart_rx_packet(packet):
    return packet.decode("utf-8").strip()


# 문제 4.
#
# I2C 7-bit 주소가 유효한지 확인하세요.
#
# address는 정수입니다.
# 유효하면 True, 아니면 False를 반환해야 합니다.
def is_valid_i2c_address(address):
    return 0x00 <= address <= 0x7F


# 문제 5.
#
# SPI 전송 프레임을 생성하세요.
#
# command는 0~255 범위의 정수입니다.
# payload는 0~255 범위의 정수 리스트입니다.
#
# 전송 프레임은 아래 순서로 구성합니다.
#
# [command, payload_length, payload...]
def make_spi_transfer_frame(command, payload):
    return [command, len(payload)] + payload
