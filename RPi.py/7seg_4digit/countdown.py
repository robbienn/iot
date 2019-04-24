import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637
#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

Display = tm1637.TM1637(23,24,tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(1)

#Display.Show([0x7f, 0,0,0])
#time.sleep(3)

def prepareNumber(number):

        result = [];
        leading = True
        last4 = str(number)[-4:].rjust(4,'0')
        for d in str(last4):
            if (d == "0") and leading:
                result.append(0x7f)
            else:
                leading = False
                result.append(int(d))
        return result

now = datetime.datetime.now().timestamp()
print(now)
print("--------------------------------")


'''

tick = datetime.datetime.now()

for i in range(1,1000,1):
    Display.Show(prepareNumber(i))
    #print (prepareNumber(i))
    time.sleep(1)

tock = datetime.datetime.now()   
diff = tock - tick    # the result is a datetime.timedelta object
print(diff.total_seconds())
'''


#GPIO.setmode(GPIO.BOARD)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Robbie"
print("Hello " + name)

while True:
    if GPIO.input(14):
       print("Door is open")
       time.sleep(2)
    if GPIO.input(14) == False:
       print("Door is closed")
       time.sleep(2)



print("--------------------------------")

'''
while(True):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ]
    Display.Show(currenttime)
    Display.ShowDoublepoint(second % 2)
    time.sleep(1)

'''