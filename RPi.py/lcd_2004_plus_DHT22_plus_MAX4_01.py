# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import Adafruit_DHT

from time import gmtime, strftime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT



# Termometer DHT22 ~ AM2302
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 17 # GPIO17 ~ PIN 11

# LCD 2004
LCD_ADDRESS = 0x3E
mylcd = RPi_I2C_driver.lcd(LCD_ADDRESS)

# MAX 4 segments -90 degrees
serial = spi(port=0, device=0, gpio=noop())

# device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
cascaded = 4
block_orientation = -90
rotate = 0
max4 = max7219(serial, cascaded=4, block_orientation = -90)


while True:

	timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

	mylcd.lcd_clear()

	mylcd.lcd_display_string("Teplota a vlhkost", 1)
	humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)    

	if humidity is not None and temperature is not None:
	    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	    temp = '{0:0.1f}*C'.format(temperature)
	    humi = '{0:0.1f}%'.format(humidity)
	    mylcd.lcd_display_string(" Teplota: " + temp, 2)
	    mylcd.lcd_display_string(" Vlhkost: " + humi, 3)
	    mylcd.lcd_display_string(" " + timestamp, 4)
	    
	    msg = timestamp + " Teplota: " + temp + " - Vlhkost: " + humi
	    print(msg)
	    show_message(max4, msg, fill="white", font=proportional(LCD_FONT))    
	    
	else:
	    print('Failed to get reading. Try again!')


	sleep(3) 


