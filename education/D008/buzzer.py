from time import sleep

from gpiozero import PWMOutputDevice

BUZZER_PIN = 18  # BCM GPIO18, physical pin 12

buzzer = PWMOutputDevice(BUZZER_PIN)

notes = [
    ("Do", 261),  # C4
    ("Re", 293),  # D4
    ("Mi", 329),  # E4
    ("Fa", 349),  # F4
    ("Sol", 392), # G4
    ("La", 440),  # A4
    ("Si", 493),  # B4
    ("Do", 523),  # C5
]

try:
    for name, freq in notes:
        print(name, freq, "Hz")

        buzzer.frequency = freq
        buzzer.value = 0.5

        sleep(0.4)

        buzzer.off()
        sleep(0.1)

finally:
    buzzer.off()
    buzzer.close()
