This guide sets up the Raspberry Pi Zero W for controlling Adafruit Dotstar LED strips/matrices.
End result: capability to control color brightness and hue via transmitter RC commands (via Mavlink), or directly via script commands.
Assumption: main MavlinkPi setup is complete.

ADAFRUIT DOTSTAR SETUP
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
https://learn.adafruit.com/adafruit-dotstar-leds/python-circuitpython

1. On pi:
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
sudo pip3 install adafruit-circuitpython-dotstar

2. Connections
Dotstar Power : external +5V supply (Adafruit estimates 60 mA draw per LED at full brightness.  64 LED = 3.84 A ... but running full brightness too long may melt things!)
Dotstar GND : external supply GND and Pi GND
Dotstar Cin : Pi SPI SCK (GPIO 19)
Dotstar Din : Pi SPI MOSI (GPIO 23)

3. Test with script:
python dotstar_simpletest.py

