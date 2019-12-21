import logging
import http.client, urllib
import Adafruit_DHT
from time import *
import datetime


logging.basicConfig(filename='/home/pi/thingspeak_thp.log',level=logging.DEBUG)

# Thingspeak
SERVER_URL = "api.thingspeak.com:80"
channel_id = 604642
write_key  = "SMYAN1ZW2XJJTHUK"

# Termometer DHT22 ~ AM2302
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 17 # GPIO17 ~ PIN 11

SLEEP_SECONDS = 20

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


temperature = 100
humidity = 50
pressure = 1111
temperature2 = 88


while(True):
	humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)    
	now = datetime.datetime.now()

	if humidity is not None and temperature is not None and pressure is not None and temperature2 is not None:        
		humidity = round(humidity, 2)	
		temperature = round(temperature, 2)
		#temp = '{0:0.1f}*C'.format(temperature)
		#humi = '{0:0.1f}%'.format(humidity)
		#pres = '{0:0.1f}kPa'.format(pressure)

		upload_thp_to_ts(temperature, humidity, pressure, temperature2, now)

	else:
		print('Failed to get reading. Try again!')
		next

	
	sleep(SLEEP_SECONDS)



log_file.close()

