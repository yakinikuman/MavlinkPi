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

# Setup mavproxy, pymavlink
pip3 install mavproxy pymavlink
apt remove modemmanager

# Build and Setup mavlink-router
apt install git
git clone https://github.com/mavlink-router/mavlink-router.git
cd mavlink-router
git submodule update --init --recursive
apt install git meson ninja-build pkg-config gcc g++ systemd python3-pip
pip3 install meson
meson setup build .
ninja -C build
ninja -C build install
mkdir /etc/mavlink-router
cp ../main.conf /etc/mavlink-router/main.conf

### TO DO - service to start mavlink-router on boot (mavlink-router already creates one but need to enable it)

# Need to reboot to enable Wifi Access Point
systemctl reboot
