Project: control LED matrix and speaker connected to Raspberry Pi Zero W, triggered by IR break-beam sensor.
These will be embedded in a valentine's day box at school - when children insert a valentine into the slot, the break-beam sensor will trigger the lights and sounds.

Need to make valentine.py executable  (chmod +x)

Need to copy valentine.service to /etc/systemd/system:
sudo cp valentine.service /etc/systemd/system/
Then: 
sudo systemctl enable valentine

This service will run the main script, valentine.py, on Pi boot up.


Expected result: display a rainbow pattern until the IR sensor is triggered (a valentine has been received), then a falling heart will display on the LED matrix(s) and a sound will play.