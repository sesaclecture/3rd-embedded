from gpiozero import PWMLED, DigitalOutputDevice
from time import sleep

# 핀 번호는 BCM 기준
pwm = PWMLED(18)               # 속도 제어 (PWM 핀)
direction = DigitalOutputDevice(23)  # 방향 제어 핀

try:
    direction.on()   # 한쪽 방향 (HIGH)
    duty = 0.0
    step = 0.1

    while True:
        pwm.value = duty   # duty cycle (0.0 ~ 1.0)
        print(f"Duty: {duty*100:.0f}%")
        sleep(1)

        duty += step
        if duty >= 1.0:
            duty = 1.0
            step = -0.1
        elif duty <= 0.0:
            duty = 0.0
            step = 0.1

except KeyboardInterrupt:
    pwm.off()
    direction.off()
    print("종료합니다.")

