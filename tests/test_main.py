from src.main import (
    gpio_level_to_state,
    make_uart_tx_packet,
    parse_uart_rx_packet,
    is_valid_i2c_address,
    make_spi_transfer_frame,
)


def test_gpio_level_to_state():
    assert gpio_level_to_state(0) == "LOW"
    assert gpio_level_to_state(1) == "HIGH"

    result = gpio_level_to_state(2)
    assert isinstance(result, str)


def test_make_uart_tx_packet():
    packet = make_uart_tx_packet("HELLO")

    assert isinstance(packet, bytes)
    assert packet.endswith(b"\n")
    assert packet.startswith(b"HELLO")

    packet = make_uart_tx_packet("TEMP:25")

    assert isinstance(packet, bytes)
    assert packet.endswith(b"\n")
    assert b"TEMP:25" in packet


def test_parse_uart_rx_packet():
    result = parse_uart_rx_packet(b"HELLO\n")

    assert isinstance(result, str)
    assert result == "HELLO"

    result = parse_uart_rx_packet(b"TEMP:25\n")

    assert isinstance(result, str)
    assert result == "TEMP:25"


def test_is_valid_i2c_address():
    assert is_valid_i2c_address(0x00) is True
    assert is_valid_i2c_address(0x68) is True
    assert is_valid_i2c_address(0x7F) is True

    assert is_valid_i2c_address(-1) is False
    assert is_valid_i2c_address(0x80) is False
    assert is_valid_i2c_address(0x100) is False


def test_make_spi_transfer_frame():
    frame = make_spi_transfer_frame(0x01, [0x10, 0x20])

    assert isinstance(frame, list)
    assert frame[0] == 0x01
    assert frame[1] == 2
    assert frame[2:] == [0x10, 0x20]

    frame = make_spi_transfer_frame(0xA0, [0x01, 0x02, 0x03])

    assert isinstance(frame, list)
    assert frame[0] == 0xA0
    assert frame[1] == 3
    assert frame[2:] == [0x01, 0x02, 0x03]
