from picamera import PiCamera
import time

camera = PiCamera() 

camera.start_preview()
time.sleep(10)
camera.capture('/home/pi/image.jpg')
camera.stop_preview()

