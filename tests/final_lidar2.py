import serial

com_port = "/dev/ttyUSB0"

ser = serial.Serial(port=com_port,baudrate=230400,timeout=5.0,bytesize=8,parity='N',stopbits=1)
b = ser.read()
tmpInt = int.from_bytes(b, 'big')
print(tmpInt)
