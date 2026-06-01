from time import sleep

from gpiozero import PWMLED

led = PWMLED(18)  # GPIO18번 핀 (BCM 번호)

try:
    while True:
        # 0.0(꺼짐) → 1.0(최대 밝기)까지 서서히 증가
        for duty in range(0, 101, 10):  # 0,10,20,...100
            led.value = duty / 100
            print(f"밝기: {duty}%")
            sleep(0.5)

        # 100% → 0%까지 서서히 감소
        for duty in range(100, -1, -10):
            led.value = duty / 100
            print(f"밝기: {duty}%")
            sleep(0.5)

except KeyboardInterrupt:
    led.off()
    print("종료합니다.")
