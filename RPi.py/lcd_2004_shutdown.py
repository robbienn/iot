# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

ADDRESS = 0x3E

mylcd = RPi_I2C_driver.lcd(ADDRESS)

mylcd.lcd_clear()

mylcd.backlight(0)
