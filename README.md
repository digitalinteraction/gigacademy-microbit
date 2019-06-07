# Lighting Prototype Kit

This repository contains the code to create a kit to teach elements of stage lighting by using BBC Microbits as physical represetations of lamps.

This can be addressed and manipulated just light real fixtures, and controlled by existing lighting hardware / software (DMX).

Currently, 128 channels are broadcast wirelessly to Microbits within range. The initial channel is changed using the buttons on each microbit. 

Each microbit mode can be set to one of by pressing both buttons together:
- Single channel White (1 neopixel)
- 3 Channel RGB (1 neopixel)
- 24 Channel 8 x RGB (8 neopixels)

## Required Hardware

- Raspberry PI (3)
- WiFi Router
- 1 BBC Microbit as a transmitter, plugged into Raspberry PI
- 1 BBC Microbit for each fixture in the prototype rig (with 1-8 neopixel LEDs)

## Setup Microbits

- Copy the `microbit/server.hex` file onto a single microbit.
- Copy the `microbit/client.hex` file onto as many *fixtures* as you need. Attach Neopixels to pins 0, 3 and GND as normal.

## Setup Server

- Attach RPI to router, and plug in server Microbit.
- Install Raspbian on Raspeberry PI, and SSH in or Open Terminal
- Install OLA Lighting Server and Python API with `sudo apt-get install ola ola-python`
- Get server code with `git clone https://github.com/digitalinteraction/gigacademy-microbit.git`
- Install Python dependencies `cd gigacademy-microbit/server && pip install -r requirements.txt`
- To start on boot, add the following line to the bottom of `.bashrc`, and setup PI to auto login to terminal on boot using `raspi-config`.

`python /home/pi/server/microbit.py`
- We also advise changing the RPI settings using `raspi-config` to wait for network on boot, which helps the OLA server start correctly.


## Configuration

- To control the lighting system you will need to add either an incoming DMX hardware channel (i.e. using a DMX dongle), or activate ACN, ARTNET or another IP protocol. This can be done using the admin panel at http://ipaddressofpi:9090

## Lamp Personalities

The proxy lamps have 3 current personalities:

Mode 1:

Single channel dimmer (0-255). Exposes as PWM signal on PIN 1.

```
|---|
|   |
|   |
```

Mode 2:

3 Channel RGB (0-255). Exposes as 3 item Neopixel string on PIN0 (rgb).


```
|---|
|---|
|   |
```

Mode 3:

26 Channel 8 segment RGB (0-255). Channel 1 controls master dimmer (0-255). Each consecutive 3 channels is RGB for segment. Channel 26 is ignored.  Exposes as 8 item Neopixel string on PIN0 (rgb).

```
|---|
|---|
|---|
```