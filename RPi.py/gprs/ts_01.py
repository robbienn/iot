import http.client, urllib

# Thingspeak
SERVER_URL = "api.thingspeak.com:80"
channel_id = 604642
write_key  = "SMYAN1ZW2XJJTHUK"

def upload_thp_to_ts(temperature, humidity, pressure):

	params = urllib.parse.urlencode({'field1': temperature, 'field2': humidity, 'field3': pressure, 'key': write_key})    
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = http.client.HTTPConnection(SERVER_URL)
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print (response.status, response.reason)
		data = response.read()
		conn.close()
		print("Connection to", SERVER_URL, "successfull")
	except:
		print("Connection to", SERVER_URL, "failed")

temperature = 100
humidity = 50
pressure = 1111

upload_thp_to_ts(temperature, humidity, pressure)




