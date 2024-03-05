import smbus2 as smbus
import time

MAX30102_ADDRESS = 0x57

REG_INT_STATUS = 0x00
REG_FIFO_DATA = 0x09
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED_CONFIG = 0x0C

MODE_CONFIG_VALUE = 0x03
SPO2_CONFIG_VALUE = 0x27 
LED_CONFIG_VALUE = 0x47   

bus = smbus.SMBus(1)

def init_max30102():
    bus.write_byte_data(MAX30102_ADDRESS, REG_MODE_CONFIG, MODE_CONFIG_VALUE)
    bus.write_byte_data(MAX30102_ADDRESS, REG_SPO2_CONFIG, SPO2_CONFIG_VALUE)
    bus.write_byte_data(MAX30102_ADDRESS, REG_LED_CONFIG, LED_CONFIG_VALUE)

def read_max30102_data():
    data = bus.read_i2c_block_data(MAX30102_ADDRESS, REG_FIFO_DATA, 6)
    ir = (data[3] << 16 | data[4] << 8 | data[5]) & 0x03FFFF
    red = (data[0] << 16 | data[1] << 8 | data[2]) & 0x03FFFF
    return red, ir

try:
    init_max30102()
    while True:
        red, ir = read_max30102_data()
        print(f"Red: {red}, IR: {ir}")
        time.sleep(1)
except KeyboardInterrupt:
     pass
finally:
    print("Fin du programme.")