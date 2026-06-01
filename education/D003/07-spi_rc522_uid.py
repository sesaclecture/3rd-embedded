# 11-rc522_uid.py
import time

from rc522_wrapper import RC522

r = RC522()
try:
    while True:
        uid = r.read_uid()
        atqa = r.tag_present()
        if uid and atqa:
            print(f"Tag: {atqa.hex()} UID: {uid.hex()}")
            time.sleep(1.0)
        time.sleep(0.15)
finally:
    r.close()
