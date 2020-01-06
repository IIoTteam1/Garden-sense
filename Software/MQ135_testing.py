import time, sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def action(pin):
    print 'Danger!'
    return

GPIO.add_event_detect(16, GPIO.RISING)
GPIO.add_event_callback(16, action)

try:
    if True:
        print 'Safe.'
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()