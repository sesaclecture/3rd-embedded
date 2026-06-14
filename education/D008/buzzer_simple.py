from time import sleep

from gpiozero import PWMOutputDevice

BUZZER_PIN = 18  # BCM GPIO18, physical pin 12

buzzer = PWMOutputDevice(BUZZER_PIN, frequency=1000)

try:
    print("Duty 20%")
    buzzer.value = 0.2
    sleep(1)

    print("Duty 50%")
    buzzer.value = 0.5
    sleep(1)

    print("Duty 80%")
    buzzer.value = 0.8
    sleep(1)

    print("OFF")
    buzzer.off()

finally:
    buzzer.off()
    buzzer.close()
