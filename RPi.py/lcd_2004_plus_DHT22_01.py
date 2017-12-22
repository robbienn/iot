# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import Adafruit_DHT

# Termometer DHT22 ~ AM2302
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 17 # GPIO17 ~ PIN 11

# LCD 2004
LCD_ADDRESS = 0x3E
mylcd = RPi_I2C_driver.lcd(LCD_ADDRESS)


mylcd.lcd_clear()


mylcd.lcd_display_string("Teplota a vlhkost", 1)
humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)    

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    temp = '{0:0.1f}*C'.format(temperature)
    humi = '{0:0.1f}%'.format(humidity)
    mylcd.lcd_display_string(" Teplota: " + temp, 2)
    mylcd.lcd_display_string(" Vlhkost: " + humi, 3)
    mylcd.lcd_display_string("--------------------", 4)
else:
    print('Failed to get reading. Try again!')


sleep(12) # 2 sec delay

mylcd.lcd_clear()

mylcd.backlight(0)
