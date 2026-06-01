import board, busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(72, 40, i2c, addr=0x3C)  # ★ 72x40
oled.fill(0); oled.show()

img = Image.new("1", (72, 40))
d = ImageDraw.Draw(img)
d.text((0,0), "72x40 OK", fill=255)
oled.image(img); oled.show()
