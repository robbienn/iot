import logging
import http.client, urllib
import Adafruit_DHT
#from Adafruit_BME280 import *


import smbus2
import bme280

from time import *
import datetime
import RPi_I2C_driver

SLEEP_SECONDS = 600

logging.basicConfig(filename='/home/pi/thingspeak_thp.log',level=logging.DEBUG)

# Thingspeak
SERVER_URL = "api.thingspeak.com:80"
channel_id = 604642
write_key  = "SMYAN1ZW2XJJTHUK"

# Termometer DHT22 ~ AM2302
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 17 # GPIO17 ~ PIN 11

# LCD 2004
LCD_ADDRESS = 0x3E
mylcd = RPi_I2C_driver.lcd(LCD_ADDRESS)
mylcd.lcd_clear()

# GY BM 280 
#PRESSURE_ADDRESS = 0x76
#pressure_sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, address=PRESSURE_ADDRESS)
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)


def upload_thp_to_ts(temperature, humidity, pressure, temperature2, timestamp):

	to_log = str(timestamp) + ' - T1={0:0.1f}*C H={1:0.1f}% P={2:0.1f} T2={3:0.1f}*C'.format(temperature, humidity, pressure, temperature2)

	params = urllib.parse.urlencode(
		{'field1': temperature, 'field2': humidity, 'field3': pressure, 'field4': temperature2, 'field5': timestamp, 'key': write_key})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = http.client.HTTPConnection(SERVER_URL)
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		#print (response.status, response.reason)
		data = response.read()
		conn.close()
		to_log += " - " + str(response.status) + " " + str(response.reason)
	except:
		to_log += " - Connection to " + SERVER_URL + " failed!"

	print(to_log)
	logging.info(to_log)


def show_on_lcd(temperature, humidity, pressure, temperature2, timestamp):
	mylcd.lcd_display_string(str(timestamp)[:19], 1)
	mylcd.lcd_display_string(" T1: " + temperature + " - T2: " + temperature2, 2)
	mylcd.lcd_display_string(" Vlhkost:  " + humidity, 3)
	mylcd.lcd_display_string(" Tlak:     " + pressure, 4)
	

while(True):
	now = datetime.datetime.now()

	humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)    

	bme_data = bme280.sample(bus, address, calibration_params)
	pressure = bme_data.pressure
	temperature2 = bme_data.temperature

	if humidity is not None and temperature is not None and pressure is not None and temperature2 is not None:        
		
		temperature = round(temperature, 2)
		humidity = round(humidity, 2)
		pressure = round(pressure, 2)
		temperature2 = round(temperature2, 2)

		# the compensated_reading class has the following attributes
		#print(bme_data.id)
		#print(bme_data.timestamp)
		#print(bme_data.temperature)
		#print(bme_data.pressure)
		#print(bme_data.humidity)
		#print(bme_data)

		upload_thp_to_ts(temperature, humidity, pressure, temperature2, now)
		show_on_lcd('{0:0.1f}'.format(temperature), '{0:0.1f}%'.format(humidity), '{0:0.1f}kPa'.format(pressure), '{0:0.1f}'.format(temperature2), now)

	else:
		print('Failed to get reading. Try again!')
		next
	
	sleep(SLEEP_SECONDS)

log_file.close()

