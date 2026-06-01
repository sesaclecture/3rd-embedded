# 09-ssd1306_menu_gpiozero.py
import time

import adafruit_ssd1306
import board
import busio
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

# OLED (72x40, I2C 0x3C)
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(72, 40, i2c, addr=0x3C)
font = ImageFont.load_default()

menus = [("Noodle", 3500), ("Kimbab", 2500), ("DDuckBBokGi", 4000)]
idx = 0
mode = "menu"  # "menu" or "price"

btn = Button(18, pull_up=True, bounce_time=0.05)  # GPIO18 한 개만 사용
press_t = 0.0
HOLD_SEC = 0.8

def draw():
    img = Image.new("1", (oled.width, oled.height))
    d = ImageDraw.Draw(img)
    name, price = menus[idx]
    if mode == "menu":
        d.text((2, 12), f"> {name}", font=font, fill=255)
    else:  # "price"
        d.text((2, 6),  name,         font=font, fill=255)
        d.text((2, 22), f"{price}won", font=font, fill=255)
    oled.image(img); oled.show()

def on_press():
    global press_t
    press_t = time.monotonic()

def on_release():
    global idx, mode
    dt = time.monotonic() - press_t
    if mode == "menu":
        if dt >= HOLD_SEC:        # 길게 누름 → 가격 표시
            mode = "price"
        else:                     # 짧게 누름 → 다음 메뉴(원형)
            idx = (idx + 1) % len(menus)
    else:                         # price 모드에서 아무 길이든 → 메뉴로 복귀
        mode = "menu"
    draw()

btn.when_pressed = on_press
btn.when_released = on_release

draw()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    oled.fill(0); oled.show()
