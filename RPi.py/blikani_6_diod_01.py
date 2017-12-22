import RPi.GPIO as gpio
import time
###############################


gpio.setwarnings(False)

ledPins = [23,24,25,26,27,22]
sleepTime = 0.2

gpio.setmode(gpio.BCM)
for ledPin in ledPins:
    gpio.setup(ledPin, gpio.OUT)
    gpio.output(ledPin, gpio.LOW)


while True:
    for ledPin in ledPins:
        gpio.output(ledPin, gpio.HIGH)
        time.sleep(sleepTime)
        gpio.output(ledPin, gpio.LOW)
        time.sleep(sleepTime)
        
