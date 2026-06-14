from time import sleep

from gpiozero import PWMOutputDevice

BUZZER_PIN = 18  # BCM GPIO18, physical pin 12

buzzer = PWMOutputDevice(BUZZER_PIN)

# C major scale
NOTE = {
    "C4": 262,  # 도
    "D4": 294,  # 레
    "E4": 330,  # 미
    "F4": 349,  # 파
    "G4": 392,  # 솔
    "A4": 440,  # 라
    "B4": 494,  # 시
    "C5": 523,  # 높은 도
    "REST": 0,  # 쉼표
}

# Twinkle Twinkle Little Star melody
melody = [
    ("C4", 0.4), ("C4", 0.4), ("G4", 0.4), ("G4", 0.4),
    ("A4", 0.4), ("A4", 0.4), ("G4", 0.8),

    ("F4", 0.4), ("F4", 0.4), ("E4", 0.4), ("E4", 0.4),
    ("D4", 0.4), ("D4", 0.4), ("C4", 0.8),

    ("G4", 0.4), ("G4", 0.4), ("F4", 0.4), ("F4", 0.4),
    ("E4", 0.4), ("E4", 0.4), ("D4", 0.8),

    ("G4", 0.4), ("G4", 0.4), ("F4", 0.4), ("F4", 0.4),
    ("E4", 0.4), ("E4", 0.4), ("D4", 0.8),

    ("C4", 0.4), ("C4", 0.4), ("G4", 0.4), ("G4", 0.4),
    ("A4", 0.4), ("A4", 0.4), ("G4", 0.8),

    ("F4", 0.4), ("F4", 0.4), ("E4", 0.4), ("E4", 0.4),
    ("D4", 0.4), ("D4", 0.4), ("C4", 0.8),
]


def play_note(note_name, duration):
    freq = NOTE[note_name]

    if freq == 0:
        buzzer.off()
        sleep(duration)
        return

    buzzer.frequency = freq
    buzzer.value = 0.5

    sleep(duration)

    buzzer.off()
    sleep(0.05)


try:
    for note_name, duration in melody:
        print(note_name, duration)
        play_note(note_name, duration)

finally:
    buzzer.off()
    buzzer.close()
