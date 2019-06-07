from microbit import *
import neopixel
import radio
import time
import machine

mode = 1
used = 3
address = 1
lasttime = 0
isasleep = False
timeoutseconds = 60

loadingImg = [Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, Image.CLOCK7, Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11, Image.CLOCK12]

currentvalues = []

strip = neopixel.NeoPixel(pin0, 8)
pin1.set_analog_period(10)

def setLights(data):
    global mode
    global strip
    if mode == 2:
        for i in range(1, 24, 3):
            # for a strip of 8 lights:
            strip[i // 3] = ((data[i] * data[0]) // 255, (data[i + 1] * data[0]) // 255, (data[i + 2] * data[0]) // 255)
        strip.show()
    if mode == 1:
        for i in range(0, 8, 1):
            # for a strip of 8 lights:
            strip[i] = (data[0], data[1], data[2])
        strip.show()
    if mode == 0:
        for i in range(0, 8, 1):
            strip[i] = (data[0], data[0], data[0])
        pin1.write_analog(data[0]*2)
        strip.show()

def showAddress(address):
    display.scroll(str(address) + " ", wait=False, loop=True)

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

def gotosleep():
    global isasleep
    isasleep = True
    radio.off()
    display.off()
    strip.clear()
    pin1.write_analog(0)

load()
radio.on()
display.on()
radio.config(length=66)
display.show(loadingImg, delay=50)
showAddress(address)
updateMode()

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



while True:

    if isasleep:
        # Check for wakeup Button:
        if button_a.was_pressed() or button_b.was_pressed():
            machine.reset()
            break

        time.sleep_ms(100)
    else:

        # Check for sleep:
        if time.ticks_add(lasttime, timeoutseconds * 1000) < time.ticks_ms():
            gotosleep()

        # 2 Button Switch for changing mode:
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
            display.show(loadingImg, delay=50)
            showAddress(address)
        else:

            #Decrement Address
            if button_b.was_pressed():
                if address < 254 - 3:
                    address += 1

                showAddress(address)
                strip.clear()
                currentvalues = [0]*used
                setLights(currentvalues)
                save()

            #Increment Address
            if button_a.was_pressed():
                if address > 1:
                    address += -1

                showAddress(address)
                strip.clear()
                currentvalues = [0]*used
                setLights(currentvalues)
                save()

        if not isasleep:

            #Receive radio
            msg = radio.receive_bytes()
            if msg is not None:
                lasttime = time.ticks_ms()
                mybank = (address-1) // 32
                if mybank == msg[0]:

                    for i in range(0, min(used, (32 - ((address-1) % 32)))):
                        currentvalues[i] = msg[1 + ((address-1) % 32) + i]

                    setLights(currentvalues)

                # overlap into next bank:
                if (((address - 1) % 32) + used > 32):
                    # if it matches the next bank up
                    startindex = (32 - ((address - 1) % 32))
                    endindex = used - startindex

                    if mybank+1 == msg[0]:
                        for i in range(0, endindex):
                            currentvalues[i + startindex] = msg[1 + i]
                        setLights(currentvalues)

