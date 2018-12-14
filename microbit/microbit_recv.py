from microbit import *
import neopixel
import radio

mode = 0
used = 1
address = 1

currentvalues = []

strip = neopixel.NeoPixel(pin0, 8)
pin1.set_analog_period(10)
#pin1.write_digital(1)
#pin1.write_analog(512)

def setLights(data):
    global mode
    global strip
    global counter
    counter = counter + 1
    if mode == 2:
        for i in range(1, 24, 3):
            # for a strip of 8 lights:
            strip[i // 3] = ((data[i] * data[0]) // 255, (data[i + 1] * data[0]) // 255, (data[i + 2] * data[0]) // 255)
            #strip[i // 3] = (data[i], data[i + 1], data[i + 2])
            # strip[i // 3] = (255, 255, 0)
        strip.show()
    if mode == 1:
        for i in range(0, 8, 1):
            # for a strip of 8 lights:
            strip[i] = (data[0], data[1], data[2])
        strip.show()
    if mode == 0:
        for i in range(0, 8, 1):
            # display.show(data[0],wait=False)
            strip[i] = (data[0], data[0], data[0])
            #pin1.write_analog(512)
        pin1.write_analog(data[0]*2)
        strip.show()

def updateMode():
    global mode
    global used
    global currentvalues
    if mode == 0:
        used = 1
    if mode == 1:
        used = 3
    if mode == 2:
        used = 26
    currentvalues = [0]*used

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

counter = 0

mode1img = Image(
    '00000:'
    '09990:'
    '00000:'
    '00000:'
    '00000:')
    
mode2img = Image(
    '00000:'
    '09990:'
    '09990:'
    '00000:'
    '00000:')
    
mode3img = Image(
    '00000:'
    '09990:'
    '09990:'
    '09990:'
    '00000:')

loadingImg = [Image.CLOCK1,Image.CLOCK2,Image.CLOCK3,Image.CLOCK4,Image.CLOCK5,Image.CLOCK6,Image.CLOCK7,Image.CLOCK8,Image.CLOCK9,Image.CLOCK10,Image.CLOCK11,Image.CLOCK12]

while True:
    
    if button_a.is_pressed() and button_b.is_pressed():
        
        mode = mode + 1
        if (mode > 2):
            mode = 0
        updateMode()
        save()
        if mode == 0:
            display.show(mode1img)
        if mode == 1:
            display.show(mode2img)
        if mode == 2:
            display.show(mode3img)
        sleep(800)
        button_a.was_pressed()
        button_b.was_pressed()
        display.show(loadingImg,delay=50)
        display.show(address, wait=False, loop=True)
        
    else:
    
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
        mybank = address // 32
        #if (msg[0] == 0):
        #    display.clear()
        #display.set_pixel(msg[0] % 5, msg[0] // 5, 9)
        if mybank == msg[0]:
            for i in range(0, 1 + min(used-1,(32 - (address % 32)))):
                currentvalues[i] = msg[(address % 32) + i]
                
            setLights(currentvalues)
        
        