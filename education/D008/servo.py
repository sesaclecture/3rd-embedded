from time import sleep

from gpiozero import AngularServo, Device
from gpiozero.pins.lgpio import LGPIOFactory

# Pi 5용 lgpio 백엔드 사용
Device.pin_factory = LGPIOFactory()

servo = AngularServo(
    18,                 # GPIO18 (PWM 가능 핀)
    min_angle=0, max_angle=180,
    min_pulse_width=0.0005,  # 0.5 ms
    max_pulse_width=0.0024   # 2.4 ms
)

angle = 0
step = 10
try:
    while True:
        servo.angle = angle
        print(f"angle={angle}")
        sleep(0.5)

        angle += step
        if angle >= 180:
            angle = 180
            step = -10
        elif angle <= 0:
            angle = 0
            step = 10
except KeyboardInterrupt:
    pass
finally:
    try:
        servo.detach()
    except Exception:
        pass
