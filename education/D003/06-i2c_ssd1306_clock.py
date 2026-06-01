# 07-i2c_ssd1306_clock_simple.py
import time

import adafruit_ssd1306
import board
import busio
from PIL import Image, ImageDraw, ImageFont

# 디스플레이 초기화 (72x40, 주소 0x3C)
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(72, 40, i2c, addr=0x3C)

# 화면 지우기
oled.fill(0)
oled.show()

# 기본 폰트 (작아도 간단히 표시 가능)
font = ImageFont.load_default()

while True:
    # 새 캔버스
    img = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(img)

    # 현재 시간 (시:분)
    now = time.strftime("%H:%M:%S")
    draw.text((4, 12), now, font=font, fill=255)

    oled.image(img)
    oled.show()
    time.sleep(0.2)
