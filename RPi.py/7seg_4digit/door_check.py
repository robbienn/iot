import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637

SPEAKERPORT = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKERPORT, GPIO.OUT)

# Number of steps from A3. Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
NOTES = {
'A2': -12.0, 'Bb2': -11.0, 'B2': -10.0, 'C3': -9.0, 'Db3': -8.0, 'D3': -7.0, 
'Eb3': -6.0, 'E3': -5.0, 'F3': -4.0, 'Gb3': -3.0, 'G3': -2.0, 'Ab3': -1.0, 
'A3': 0.0, 'Bb3': 1.0, 'B3': 2.0, 'C4': 3.0, 'Db4': 4.0, 'D4': 5.0, 'Eb4': 6.0, 
'E4': 7.0, 'F4': 8.0, 'Gb4': 9.0, 'G4': 10.0, 'Ab4': 11.0, 'A4': 12.0, 'Bb4': 13.0, 
'B4': 14.0, 'C5': 15.0, 'Db5': 16.0, 'D5': 17.0, 'Eb5': 18.0, 'E5': 19.0, 'F5': 20.0, 'Gb5': 21.0, 'G5': 22.0, 'Ab5': 23.0}

# LCD 4 x 7seg
# CLK -> GPIO23 (Pin 16)
# Di0 -> GPIO24 (Pin 18)
Display = tm1637.TM1637(23,24,tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(1)


# door magnet
# GPIO.setmode(GPIO.BOARD)
DOOR_MAGNET_PIN = 14
GPIO.setup(DOOR_MAGNET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#Display.Show([0x7f, 0,0,0])
#time.sleep(3)

def tone(note, duration):
    
    # Font: http://www.phy.mtu.edu/~suits/NoteFreqCalcs.html
    frequency = 440.0 * (1.05946309435929530984310531 ** NOTES[note])
    
    p = GPIO.PWM(SPEAKERPORT, frequency)    # 50 Hertz PWM
    p.start(50) #Duty cicle: 50%
    time.sleep(duration)
    p.stop()
    time.sleep(0.01)

def opened_sound():
    tone('C3', 0.16)
    tone('D3', 0.25)
    tone('E3', 0.34)
    tone('F3', 0.43)
    tone('G3', 0.52)

def closed_sound():
    tone('G3', 0.02)
    tone('F3', 0.43)
    tone('E3', 0.34)
    tone('D3', 0.25)
    tone('C3', 0.16)



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


def showTime():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ]
    Display.Show(currenttime)
    Display.ShowDoublepoint(second % 2)
    time.sleep(1)


def showTimeOpened(startTime):
    print("AHOJ")
    timeOpened = datetime.datetime.now() - startTime
    print("TimeOpened: ", timeOpened)
    secondsOpened = timeOpened.seconds
    print("TimeDelta seconds: ", secondsOpened)
    Display.Show(prepareNumber(secondsOpened))
    

def isDoorOpen():    
    if GPIO.input(DOOR_MAGNET_PIN):
        #print("Door is open")
        result = True
    else:
        result = False
        #print("Door is closed")
    return result

now = datetime.datetime.now().timestamp()
print(now)
print("--------------------------------")


wasOpened = False

while True:
    doorOpened = isDoorOpen()
    if not doorOpened and wasOpened:
        closed_sound()
    if doorOpened:
        if not wasOpened:
            doorOpenedAt = datetime.datetime.now()
            print("Dvere otevreny v:", doorOpenedAt)
            wasOpened = True
            opened_sound()
        showTimeOpened(doorOpenedAt)
    else:    
        showTime()
        wasOpened = False
    time.sleep(500/1000)



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



print("--------------------------------")

