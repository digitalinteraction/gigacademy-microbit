from microbit import *
import radio
import micropython

uart.init(115200)
# disable ctl-c interrupt in data stream
micropython.kbd_intr(-1)

radio.on()
radio.config(length=65)

buffer = bytearray(65)

display.show(Image.DIAMOND_SMALL)
value = 0

counter = 0

while (True):
 
    if button_b.was_pressed():
        value = value + 1
        buffer[1] = value
        radio.send_bytes(bytes([0, value, 0, 0]))
        
    if button_a.was_pressed():
        value = value - 1
        buffer[1] = value
        radio.send_bytes(bytes([0, value, 0, 0]))
 
    dat = uart.read(33)
    if dat is not None:
        uart.write(dat[0:1])
        if len(dat) == 33:
            
            if (dat[0] == 0):
                display.clear()
                
            radio.send_bytes(dat)
            
            display.set_pixel(dat[0] % 5, dat[0] // 5, 9)
            
            counter = counter + 1
            
            #if (counter % 6 == 0):
            #    display.set_pixel(0, 0, 9)
            #if (counter % 6 == 1):
            #    display.set_pixel(0, 0, 0)