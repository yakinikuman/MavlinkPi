import RPi.GPIO as GPIO

BEAM_PIN = 22

def break_beam_callback(channel):
    if GPIO.input(BEAM_PIN):
        print("beam unbroken")
    else:
        print("beam broken")

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(BEAM_PIN, GPIO.IN)
GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)
#GPIO.add_event_detect(BEAM_PIN, GPIO.RISING, callback=break_beam_callback)
message = input("Press enter to quit\n\n")

#while True:
#	if GPIO.input(BEAM_PIN):
#		print("beam ok")
#	else:
#		print("beam break")

GPIO.cleanup()

