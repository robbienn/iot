import serial   
import os, time
 

# Enable Serial Communication
port = serial.Serial("/dev/serial0", baudrate=115200, timeout=1, rtscts=0)

print ("Zaciname")
print ("-----------------------")


def sendCommand(cmd):
	print ("CMD:", cmd)
	cmd += '\r\n';

	port.write(cmd.encode())
	time.sleep(0.1)
	output = []
	while port.inWaiting() > 0:
		output_line = port.readline().strip()
		output_line_str = str(output_line, 'ascii')
		if output_line_str != '' and output_line_str != '\r\n':
			output.append(output_line_str)
			#print("[", output_line_str, "]")
	printResponse(output)
 

def printResponse(output):
	for output_line in output:
		print (output_line)
	print("-")

sendCommand('AT')
sendCommand("ATI")
sendCommand('AT+CSQ')
sendCommand('AT+CCID')
sendCommand('AT+CCID')
sendCommand('AT+CREG?')


print("-----------------------")
print("Koncime")
