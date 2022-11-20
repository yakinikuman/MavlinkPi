# Usage:
# ./ip_forward.sh eth0 usb0
# Where "eth0" is the local interface with an internet connection,
# And "usb0" is the local interface to which you want to provide the internet connection.

set -x # echo commands as executed
sysctl -w net.ipv4.ip_forward=1
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -i $2 -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -o $1 -j MASQUERADE
iptables -A FORWARD -i $1 -o $2 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $2 -o $1 -j ACCEPT
