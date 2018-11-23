from ola.ClientWrapper import ClientWrapper
import serial
from time import sleep
import time
from ratelimit import limits

counter = 0

@limits(calls=40, period=1)
def NewData(data):
    global counter
    counter = counter + 1
    #if counter % 5 == 0:
    loop = len(data) // 32
    for i in range(0,4):
        buf = data[i*32:i*32 + 32]
        buf.insert(0,i)
	#print len(buf)
        ser.write(buf)
	while True:
		incoming = ord(ser.read(1)[0])
		# print '> ' + str(incoming) + ' == ' + str(buf[0])
		if incoming == buf[0]:
			break
        # sleep(0.2)
    
def NewDataCall(data):
    try:
        # print(".")
        NewData(data)
    except:
        print("X")

ser = serial.Serial(port='/dev/ttyACM0',baudrate=115200, timeout=None)
print("Using: "+ser.name)
universe = 1
wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(universe, client.REGISTER, NewDataCall)
wrapper.Run()