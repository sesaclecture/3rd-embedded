from time import sleep

from gpiozero import AngularServo, Device
from gpiozero.pins.lgpio import LGPIOFactory

# lgpio 백엔드 사용
Device.pin_factory = LGPIOFactory()

# SG90 서보 제어
servo = AngularServo(
    18, min_angle=0, max_angle=180,
    min_pulse_width=0.0005,  # 0.5ms
    max_pulse_width=0.0024   # 2.4ms
)

try:
    servo.angle = 90   # 90도 위치로 이동
    print("서보를 90도로 이동시켰습니다.")
    sleep(2)           # 2초 대기 (서보가 도달할 시간)
finally:
    try:
        servo.detach() # 신호 해제(휴식)
    except Exception:
        pass
