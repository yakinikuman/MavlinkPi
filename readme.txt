This is a collection of instructions and scripts for setting up a Raspberry Pi Zero W as a companion computer for MAVLink-capable drone flight controllers.

Functionality:
- ability to ssh into the Pi over USB (Pi's address: 172.16.0.1)
- ability to share (Linux) host computer's internet with the Pi over USB
- Mavlink packets available on Pi's UDP port 14550 for local use
- Pi sets up an open Wifi access point called "MavlinkPi".  Only one client is allowed to connect at a time, and that client gets IP 10.0.0.0
- Mavlink packets fowarded to Wifi client 10.0.0.0 on UDP port 14550.  This allows use of a Mavlink-capable GCS, such as QGroundControl or Mission Planner.

SETUP ETHERNET OVER USB
The first section installs a fresh version of Raspberry Pi OS and sets up USB gadget mode (ethernet-over-USB).  After this section is complete, the host computer will be able to ssh to the Pi over USB, and the Pi will be able to use the host computer's internet connection.

1) Install "Raspberry Pi OS Lite 32-bit" with rpi-imager (see https://www.raspberrypi.com/software/)
Under options, enable "set hostname" (leave as raspberrypi.local), enable SSH, and set password.  Leave username as "pi" and do not set wifi.
After flashing is complete, don't eject the SD card.  We need to add/change some files on it first.

2) On SD card: add to end of /boot/config.txt:
#For use of micro USB as Ethernet gadget
dtoverlay=dwc2
#Enable UART
enable_uart=1
# Use PL011 UART instead of mini-UART (will trade with bluetooth)
dtoverlay=miniuart-bt
# Button shutdown
dtoverlay=gpio-shutdown,gpio_pin=21,gpio_pull=down

3) On SD card: Add to /boot/cmdline.txt, after "rootwait":
modules-load=dwc2,g_ether g_ether.dev_addr=12:22:33:44:55:66 g_ether.host_addr=16:22:33:44:55:66 net.ifnames=0

Remove from /boot/cmdline.txt (this disables the serial console, which can interfere with Mavlink's use of the UART):
console=serial0,115200

4) On SD card: Add to /rootfs/etc/dhcpcd.conf (sets static IP addresses on Pi)
interface usb0
    static ip_address=172.16.0.1/24
    static routers=172.16.0.0
    static domain_name_servers=8.8.8.8
interface wlan0
    static ip_address=10.0.0.1/24
    nohook wpa_supplicant

5) On SD card: Copy full MavlinkPi folder to /rootfs/home/pi

LINUX
6) Insert SD card into the Pi and connect to host computer via USB (use the port marked "USB", not "PWR IN").  

Be patient - the pi needs several seconds to fully boot up, particularly on first boot after SD card flash.

Check if connected by running "lsusb" on host computer; should see something like:
Bus 001 Device 117: ID 0525:a4a2 Netchip Technology, Inc. Linux-USB Ethernet/RNDIS Gadget

Or run "ifconfig -a"; should see a new "usb0" interface (or similarly named - If usb0 interface is getting a different name on host computer, substitute that name in the following instructions.  Or, you may be able to stop the host computer from renaming the interface: https://askubuntu.com/questions/1350862/drivers-renaming-network-interfaces-is-there-a-way-to-prevent-it)

If none of these checks pass, try a different USB cable or check previous steps.  

7) On host computer: set the usb0 interface to a static IP of 172.16.0.0/24

8) On host computer: 

sudo ./ip_forward.sh eth0 usb0

The ip_forward script allows the pi to use the host computer's internet connection.  The first argument is the host computer's interface with internet.  The second argument is the host computer's interface to the Pi over USB.
This script must be re-executed if the host computer is rebooted.


9) On host computer: 
ssh pi@172.16.0.1
and log in with the password from step 1
Now you are on the Pi.

10) On pi: 
ping google.com  
This test of internet connectivity should succeed.  If it doesn't stop and fix the issue.  Check that the host has internet connectivity.  Check that preceding steps (particularly the ip_forward script) were completed.  Only proceed when the pi has internet connectivity.


SET UP PI WIFI ACCESS POINT AND MAVLINK-ROUTER
After this, the Pi will create a Wifi network called MavlinkPi.  You can connect to this from a PC; the Pi has address 10.0.0.1 on this network.
The Pi will be routing Mavlink packets to the host computer over both USB and Wifi.
Host computer should UDP listen on either of these:
172.16.0.0:14550
10.0.0.0:14550  ---- this is going to be more typical use case


1) ssh to pi, then:
cd MavlinkPi
sudo ./setup.sh

2) Pi will install lots of stuff, then reboot.  When pi comes back online, it should broadcast an open "MavlinkPi" network.
Mavlink packets will be routed to 10.0.0.0 and 172.16.0.0, both on port 14550
Make sure connected Flight Controller's baud rate matches main.conf

TESTED WITH
Raspberry Pi OS Lite 9/22/2022
mavlink-router 3 (https://github.com/mavlink-router/mavlink-router/commit/b24aad6c739f8d162aa4dbc5c55ff75cc8935c10)
