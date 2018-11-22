from microbit import *
import neopixel
import radio

mode = 2
used = 1
address = 1

strip = neopixel.NeoPixel(pin0, 8)

def setLights(data):
    global mode
    global strip
    global counter
    counter = counter + 1
    if mode == 2:
        for i in range(0, 24, 3):
            # for a strip of 8 lights:
            strip[i // 3] = (data[i], data[i + 1], data[i + 2])
            # strip[i // 3] = (255, 255, 0)
            strip.show()
    if mode == 1:
        strip[0] = (data[0], data[1], data[2])
        strip.show()
    if mode == 0:
        # display.show(data[0],wait=False)
        strip[0] = (data[0], data[0], data[0])
        strip.show()

def updateMode():
    global mode
    global used
    if mode == 0:
        used = 1
    if mode == 1:
        used = 3
    if mode == 2:
        used = 24

def save():
    global mode
    global address
    with open('settings', 'w') as set:
        set.write(str(address)+"\n"+str(mode))
        
def load():
    global mode
    global address
    try:
        with open('settings', 'r') as set:
            dat = set.read().split("\n")
            address = int(dat[0])
            mode = int(dat[1])
            updateMode()
    except Exception:
        print('FNF')

def update(buffer):
    global used
    global address
    bank = buffer[0] * 16
    if address > bank and address < bank + 16:
        setLights(buffer.slice(address - bank, (address - bank) + used))

load()
radio.on()
radio.config(length=65)
display.show(address, wait=False, loop=True)
updateMode()
#for i in range(0, 24, 3):
#   strip[i // 3] = (128, 64, 0)
# strip.show()

counter = 0

while True:
    if button_b.was_pressed():
        if address < 254 - 3:
            address += 1

        display.show(address, wait=False, loop=True)
        save()

    if button_a.was_pressed():
        if address > 1:
            address += -1

        display.show(address, wait=False, loop=True)
        save()

    msg = radio.receive_bytes()
    if msg is not None:
        # bank = int(msg[0]) * 64
        mybank = address // 32
        # if (msg[0] == 8):
        if (msg[0] == 0):
            display.clear()
        display.set_pixel(msg[0] % 5, msg[0] // 5, 9)
        if mybank == msg[0]:
            # counter = counter + 1
#            if counter % 10 == 0:
        # if address > bank and address < (bank + 64) and len(msg) >= ((address - bank) + used):
            setLights(msg[(address % 32):(address % 32) + used])
# 
   