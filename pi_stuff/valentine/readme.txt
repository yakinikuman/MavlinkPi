Project: control LED matrix and speaker connected to Raspberry Pi Zero W, triggered by IR break-beam sensor.
These will be embedded in a valentine's day box at school - when children insert a valentine into the slot, the break-beam sensor will trigger the lights and sounds.

Need to make valentine.py executable  (chmod +x)

Need to copy valentine.service to /etc/systemd/system:
sudo cp valentine.service /etc/systemd/system/
Then: 
sudo systemctl enable valentine

This service will run the main script, valentine.py, on Pi boot up.


Expected result: display a rainbow pattern until the IR sensor is triggered (a valentine has been received), then a falling heart will display on the LED matrix(s) and a sound will play.

Raspberry Pi Zero W wiring (pin numbers, not GPIO numbers):
1 - IR break-beam xmit/rcvr +3.3 V power (using 3.3V because output signal is same voltage as input voltage, and GPIO can only read +3.3 V)
2 - MAX98357A audio amp + 5V power
4 - Battery +5V (from USB battery pack with doctored cable).  This is also connected to APA102C LED +5V power.
6 - Battery GND
9 - IR break-beam xmit/rcvr GND
12 - MAX98357A audio amp BCLK
14 - MAX98357A audio amp GND
15 - IR break-beam rcvr output signal
19 - APA102C DIN
23 - APA102C CIN
25 - APA102C GND
35 - MAX98357A LRC
40 - MAX98357A DIN

Adafruit guides were essential to setting this up:
- APA102C 8x8 LED matrices (from aliexpress) are equivalent to Adafruit DotStars https://learn.adafruit.com/adafruit-dotstar-leds/overview
- Audio amp: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp  -- I paired this with a cheap 8ohm, 2W speaker (about 1 inch diameter)
- IR break-beam 3mm: https://learn.adafruit.com/ir-breakbeam-sensors


