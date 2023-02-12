import time
import random
import board
import adafruit_dotstar as dotstar
import sys

# Connections
# Dotstar Power : external +5V supply
# Dotstar GND : external supply GND and Pi GND
# Dotstar Cin : Pi SPI SCK (GPIO 19)
# Dotstar Din : Pi SPI MOSI (GPIO 23)

# Setup
#sudo pip3 install --upgrade adafruit-python-shell
#wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
#sudo python3 raspi-blinka.py
#sudo pip3 install adafruit-circuitpython-dotstar

# defaults
BRIGHTNESS = 0.1 # 0-1
PREDEF_COLOR = (0,0,255)
PROGRAM = 2

if len(sys.argv) == 1:
   print ("Using defaults")
elif len(sys.argv) == 2:
    PROGRAM = int(sys.argv[1])
elif len(sys.argv) == 3:
    PROGRAM = int(sys.argv[1])
    BRIGHTNESS = float(sys.argv[2])
else:
    PROGRAM = int(sys.argv[1])
    BRIGHTNESS = float(sys.argv[2])
    r = int(sys.argv[3])
    g = int(sys.argv[4])
    b = int(sys.argv[5])
    PREDEF_COLOR = (r,g,b)

NUM_LED = 128
TIME_DELAY_SEC = 3.0

# Using a DotStar Digital LED Strip connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, NUM_LED, brightness=BRIGHTNESS)

# Using a DotStar Digital LED Strip connected to digital pins
# Tried this on D5/D6 and on D23/D24 (numbers are GPIO numbers) and very slow - 10+ seconds to populate full strip whereas SPI is <<1 sec
#dots = dotstar.DotStar(board.D5, board.D6, NUM_LED, brightness=BRIGHTNESS)

def random_color():
    return random.randrange(0, 255)


########### MAIN

if PROGRAM == 1:
    print ("Program 1: Fill each dot with a random color, then repeat")
    n_dots = len(dots)
    while True:
        for dot in range(n_dots):
            #print (dot)
            dots[dot] = (random_color(), random_color(), random_color())
        time.sleep(TIME_DELAY_SEC)

if PROGRAM == 2:
    print ("Program 2: Fill all dots with same random color, then repeat")
    n_dots = len(dots)
    while True:
        color = (random_color(), random_color(), random_color())
        for dot in range(n_dots):
            dots[dot] = color
        time.sleep(TIME_DELAY_SEC)

if PROGRAM == 3:
    print ("Program 3: Fill all dots with same predefined color")
    n_dots = len(dots)
    for dot in range(n_dots):
        dots[dot] = PREDEF_COLOR

if PROGRAM == 4:
    print ("Program 4: Fill all dots with white, one by one")
    n_dots = len(dots)
    color = (255,255,255)
    for dot in range(n_dots):
        dots[dot] = (0,0,0)
    for dot in range(n_dots):
        dots[dot] = color;
        time.sleep(TIME_DELAY_SEC)
        dots[dot] = (0,0,0)

if PROGRAM == 5:
    print ("Program 5: Display a pink heart")
    pink = (255,20,147)
    heart_pix = (9,10,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,42,43,44,45,51,52)
    for dot in range(len(dots)):
        if dot in heart_pix:
            dots[dot] = pink
        else:
            dots[dot] = (0,0,0) 
 
