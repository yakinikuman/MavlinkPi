This is a collection of scripts for setting up and using a Raspberry Pi Zero W (1) as controller for Adafruit DotStar LED's, and as a bridge for MAVLink-capable drone flight controllers.

SETUP NETWORK
The first section installs a fresh version of Raspberry Pi OS and sets it up for USB gadget mode.  After this section is complete, the host computer will be able to ssh to the Pi over USB, and the Pi will share the host computer's internet connection.

1) Install "Raspberry Pi OS Lite 32-bit" with rpi-imager.  
Under options, enable "set hostname" (leave as raspberrypi.local), enable SSH, and set username/password.  Do not set wifi.

2a) After flashing complete, on SD card, add to end of /boot/config.txt:
#For use of micro USB as Ethernet gadget
dtoverlay=dwc2
#Enable UART
enable_uart=1
# Use PL011 UART instead of mini-UART (will trade with bluetooth)
dtoverlay=miniuart-bt
# Button shutdown
dtoverlay=gpio-shutdown,gpio_pin=21,gpio_pull=down

2b) Add to /boot/cmdline.txt, after "rootwait":
modules-load=dwc2,g_ether g_ether.dev_addr=12:22:33:44:55:66 g_ether.host_addr=16:22:33:44:55:66 net.ifnames=0

2c) Add to /rootfs/etc/dhcpcd.conf (sets static IP addresses on Pi)
interface usb0
    static ip_address=172.16.0.1/24
    static routers=172.16.0.0
    static domain_name_servers=8.8.8.8
interface wlan0
    static ip_address=10.0.0.1/24
    nohook wpa_supplicant

3) Copy full MavlinkPi folder to /rootfs/home/pi

LINUX
3) Insert SD card into the Pi and connect to host computer via USB (use the port marked "USB", not "PWR IN").  

Check if connected by running "lsusb" on host computer; should see something like:
Bus 001 Device 117: ID 0525:a4a2 Netchip Technology, Inc. Linux-USB Ethernet/RNDIS Gadget

Or run "ifconfig -a"; should see a new "usb0" interface (or similarly named - If usb0 interface is getting a different name on host computer, substitute that name in the following instructions.  Or, you may be able to stop the host computer from renaming the interface: https://askubuntu.com/questions/1350862/drivers-renaming-network-interfaces-is-there-a-way-to-prevent-it)

If none of these checks pass, try a different USB cable or check previous steps.  Be patient - the pi needs several seconds to fully boot up, particularly on first boot after SD card flash.

4a) On host computer, set the usb0 interface to a static IP of 172.16.0.0/24

4b) To forward the host computer's internet connection from eth0 to usb0, execute the ip_forward.sh script:
sudo ./ip_forward.sh eth0 usb0
This script must be re-executed if the host computer is rebooted.

WINDOWS
To do...

CONNECT TO PI
5) From a terminal on the host computer, 
ssh pi@172.16.0.1
and log in with the password from step 1
6) test internet connectivity with 
ping google.com  
This should succeed (assuming it succeeds on the host computer.)



SET UP PI WIFI ACCESS POINT AND MAVLINK-ROUTER
After this, the Pi will create a Wifi network called MavlinkPi.  You can connect to this from a PC; the Pi has address 10.0.0.1 on this network.
The Pi will be routing Mavlink packets to the host computer over both USB and Wifi.
Host computer should UDP listen on either of these:
172.16.0.0:14550
10.0.0.0:14550  ---- this is going to be more typical use case


1) Execute:
cd MavlinkPi
sudo ./setup.sh

2) When pi comes back online, it should broadcast an open "MavlinkPi" network.
Mavlink packets will be routed to 10.0.0.0 and 172.16.0.0, both on port 14550
Make sure connect FC baud rate matches main.conf

3) Run sudo mavlink-routerd








