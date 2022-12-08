import time
import os
from RPi import GPIO

PinButton=14

DISPLAY_ON_TIME = 60

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PinButton, GPIO.IN)

MotionDetectedTime = time.time()

def run_motion_detection_loop():
    DisplayOn=False
    i = 0
    while True:
        time.sleep(0.1)
        i += 1
        if i == 10:
            i = 0
            if DisplayOn==True:
                print(f"Time-Out: {DISPLAY_ON_TIME-round(time.time()-MotionDetectedTime)}")

        if GPIO.input(PinButton)==1:
            MotionDetectedTime = time.time()
            if DisplayOn == False:
                DisplayOn = True
                os.system('uhubctl -l 1-1 -p2 -aon')
                print("Switch ON")

        if DisplayOn:
            if time.time()-MotionDetectedTime > DISPLAY_ON_TIME:
                DisplayOn = False
                os.system('uhubctl -l 1-1 -p 2 -aoff')
                print("Switch OFF")

    GPIO.cleanup()

if __name__ == "__main__":
    try:
        run_motion_detection_loop()
    finally:
        os.system('uhubctl -l 1-1 -p2 -aon')

sys.exit()
