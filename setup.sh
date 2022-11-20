# First time setup - run with sudo ./setup.sh

set -x # echo commands as executed

# Setup Wifi Access Point
# From https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point
apt-get update
apt-get install hostapd
systemctl unmask hostapd
systemctl enable hostapd
apt-get install dnsmasq
cp dnsmasq.conf /etc/dnsmasq.conf
cp hostapd.conf /etc/hostapd/hostapd.conf
rfkill unblock wlan

# Setup mavproxy, pymavlink (not needed for mavlink-router, but nice to have for other integrations)
pip3 install mavproxy pymavlink
apt remove modemmanager -y

# Build and Setup mavlink-router
apt install git -y
git clone https://github.com/mavlink-router/mavlink-router.git
cd mavlink-router
git submodule update --init --recursive
apt install meson ninja-build pkg-config gcc g++ systemd python3-pip -y
pip3 install meson
meson setup build .
ninja -C build
ninja -C build install
mkdir /etc/mavlink-router
cp ../main.conf /etc/mavlink-router/main.conf
systemctl enable mavlink-router.service

# Need to reboot to enable Wifi Access Point and start mavlink-router service
systemctl reboot
