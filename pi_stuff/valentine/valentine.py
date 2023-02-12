#!/usr/bin/env python3
# Valentine's Day 2023
# Uses LED matrix(s), speaker, and IR break-beam sensor in elementary school student's Valentine's Day box.
# Default behavior: Just displays some pretty animation on the LED matrices.
# On IR break beam (a valentine has been inserted): play falling heart animation and say a message over the speaker
import signal
import sys
import subprocess
from animation_library import *
import RPi.GPIO as GPIO

BREAK_BEAM_PIN = 22

#############################################
# GPIO cleanup on ctrl-C
def signal_handler(signal, frame):
    print("Ctrl-C detected, exiting")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
##############################################

# setup break-beam sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(BREAK_BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# States
RAINBOW_INIT = 1
RAINBOW_CYCLE = 2
VALENTINE_RECEIVED = 3
state = RAINBOW_INIT

# main loop
num_matrices = 2
A = Animation(0,num_matrices)
ct = 0
last_beam_intact = 1
while True:
    # Check if beam has been broken (was intact and now not intact)
    beam_intact = GPIO.input(BREAK_BEAM_PIN)
    if last_beam_intact and not beam_intact:
        state = VALENTINE_RECEIVED
    last_beam_intact = beam_intact

    print(state)
    if state == RAINBOW_INIT:
        A.rainbow_init()
        state = RAINBOW_CYCLE
    elif state == RAINBOW_CYCLE:
        A.rainbow_cycle()
        state = RAINBOW_CYCLE
    elif state == VALENTINE_RECEIVED:
        #subprocess.Popen(["espeak", "Thank you!  Happy Valentines Day!"])
        #subprocess.Popen(["aplay", "/home/pi/MavlinkPi/pi_stuff/valentine/564943__anzbot__why-thank-you.wav"])
        subprocess.Popen(["aplay", "/home/pi/MavlinkPi/pi_stuff/valentine/662450__fullstacksound__big_treasure.wav"])

        hue = randf_1()
        color = hsv2rgb(hue,1,1)
        A.falling_heart(num_matrices,color)
        state = RAINBOW_INIT
    time.sleep(0.1)

GPIO.cleanup()
