import serial
from time import sleep
ser = serial.Serial('/dev/tty.usbmodem143202',115200)

while True:
    for i in range(0,8):
        # print(i)
        buffer = [0] * 65
        buffer[0] = bytes(i)
        ser.write(buffer)
        #sleep(0.1)