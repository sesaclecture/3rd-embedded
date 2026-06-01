from time import sleep

from gpiozero import Device, PWMOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory

# lgpio 백엔드 사용
Device.pin_factory = LGPIOFactory()

# GPIO18을 PWM 출력으로 사용
pwm = PWMOutputDevice(18, frequency=50)  # 50Hz 예시

try:
    pwm.value = 0.5   # duty cycle 50% (0.0 ~ 1.0)
    print("PWM 50% 출력 중...")
    sleep(10)         # 10초간 유지
finally:
    pwm.off()
