# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import Adafruit_DHT
from Adafruit_BME280 import *

# Termometer DHT22 ~ AM2302
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 17 # GPIO17 ~ PIN 11

# LCD 2004
LCD_ADDRESS = 0x3E
mylcd = RPi_I2C_driver.lcd(LCD_ADDRESS)

# GY BM 280 
PRESSURE_ADDRESS = 0x76
pressure_sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, address=PRESSURE_ADDRESS)

mylcd.lcd_clear()

while(True):

    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)    

    temperature2 = pressure_sensor.read_temperature()
    pressure = pressure_sensor.read_pressure() / 100
    #humidity2 = pressure_sensor.read_humidity()

    print 'Temp      = {0:0.3f} deg C'.format(temperature2)
    print 'Pressure  = {0:0.2f} hPa'.format(pressure)
    #print 'Humidity  = {0:0.2f} %'.format(humidity2)


    if humidity is not None and temperature is not None and pressure is not None:
        
        temp = '{0:0.1f}*C'.format(temperature)
        humi = '{0:0.1f}%'.format(humidity)
        pres = '{0:0.1f}kPa'.format(pressure)
        temp2 = '{0:0.1f}*C'.format(temperature2)

        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

        mylcd.lcd_display_string(" Teplota:  " + temp, 1)
        mylcd.lcd_display_string(" Vlhkost:  " + humi, 2)
        mylcd.lcd_display_string(" Tlak:     " + pres, 3)
        mylcd.lcd_display_string(" Teplota2: " + temp2, 4)
    else:
        print('Failed to get reading. Try again!')


    sleep(15) # 15 sec delay

    mylcd.lcd_clear()



mylcd.backlight(0)
