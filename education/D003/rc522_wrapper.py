# rc522_wrapper.py
# Raspberry Pi + RC522 (SPI) 최소 래퍼: tag_present(), read_uid()
# 초기화 보강 버전 (0x91/0x92/0xB2 칩 호환)

import time

import spidev

# RC522 레지스터/명령
CMD_IDLE       = 0x00
CMD_TRANSCEIVE = 0x0C
CMD_SOFTRESET  = 0x0F

REG_COMMAND    = 0x01
REG_COMMIRQ    = 0x04
REG_ERROR      = 0x06
REG_FIFO_DATA  = 0x09
REG_FIFO_LEVEL = 0x0A
REG_BIT_FRAM   = 0x0D
REG_MODE       = 0x11
REG_TXCONTROL  = 0x14
REG_TXASK      = 0x15
REG_RFCFG      = 0x26
REG_TMODE      = 0x2A
REG_TPRESCALER = 0x2B
REG_TRELOAD_H  = 0x2C
REG_TRELOAD_L  = 0x2D
REG_VERSION    = 0x37

REQA        = 0x26  # 7bit
ANTICOLL_CL1 = 0x93
SELECT_CL1   = 0x93
SEL_CL1      = 0x70

class RC522:
    def __init__(self, bus=0, dev=0, speed=100_000):  # ★ 기본 속도 낮게
        self.spi = spidev.SpiDev()
        self.spi.open(bus, dev)
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        self._init_14443A()          # ★ 초기화 추가
        self.antenna_on(True)

    def close(self):
        self.spi.close()

    def _addr(self, reg, read):
        a = (reg << 1) & 0x7E
        if read:
            a |= 0x80
        return a

    def _w(self, reg, val):
        self.spi.xfer2([self._addr(reg, False), val & 0xFF])

    def _r(self, reg):
        return self.spi.xfer2([self._addr(reg, True), 0x00])[1] & 0xFF

    def _setbits(self, reg, mask):
        self._w(reg, self._r(reg) | mask)

    def _clrbits(self, reg, mask):
        self._w(reg, self._r(reg) & (~mask & 0xFF))

    def _soft_reset(self):
        self._w(REG_COMMAND, CMD_SOFTRESET)
        time.sleep(0.05)

    def _init_14443A(self):
        self._soft_reset()
        # 아두이노 MFRC522 기본값 기반: 호환칩에서도 잘 먹힘
        self._w(REG_TMODE,      0x80)   # TAuto=1
        self._w(REG_TPRESCALER, 0xA9)
        self._w(REG_TRELOAD_H,  0x03)
        self._w(REG_TRELOAD_L,  0xE8)
        self._w(REG_TXASK,      0x40)   # ★ 100% ASK (중요)
        self._w(REG_MODE,       0x3D)   # CRC preset 등
        self._w(REG_RFCFG,      0x70)   # Rx 게인 강화

    def antenna_on(self, on=True):
        if on:
            self._setbits(REG_TXCONTROL, 0x03)
        else:
            self._clrbits(REG_TXCONTROL, 0x03)

    def _transceive(self, tx: bytes, bit_fram=0x00, timeout_loop=100):
        self._w(REG_COMMAND, CMD_IDLE)
        self._w(REG_COMMIRQ, 0x7F)
        self._w(REG_FIFO_LEVEL, 0x80)
        for b in tx:
            self._w(REG_FIFO_DATA, b)
        self._w(REG_BIT_FRAM, bit_fram & 0xFF)
        self._w(REG_COMMAND, CMD_TRANSCEIVE)
        self._setbits(REG_BIT_FRAM, 0x80)  # StartSend

        for _ in range(timeout_loop):
            irq = self._r(REG_COMMIRQ)
            if irq & 0x30:  # RxIRq | IdleIrq
                break
        if self._r(REG_ERROR) & 0x13:
            return b""
        n = self._r(REG_FIFO_LEVEL)
        return bytes(self._r(REG_FIFO_DATA) for _ in range(n))

    # ---------- 공개 API ----------
    def tag_present(self):
        """REQA(7bit) → ATQA 2바이트 or None"""
        self.antenna_on(True)
        resp = self._transceive(bytes([REQA]), bit_fram=0x07)
        return resp if len(resp) == 2 else None

    def read_uid(self):
        """
        단순 CL1 안티콜리전 (4바이트 UID 가정).
        """
        if not self.tag_present():
            return None
        antic = self._transceive(bytes([ANTICOLL_CL1, 0x20]))
        if len(antic) < 5:
            return None
        uid4 = antic[:5]  # 4 UID + BCC
        frame = bytes([SELECT_CL1, SEL_CL1]) + uid4
        _ = self._transceive(frame)  # CRC는 생략
        return uid4[:4]
