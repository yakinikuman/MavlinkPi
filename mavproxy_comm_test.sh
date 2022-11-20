# Meant to be run on pi, when connected to flight controller over UART
# Should see a successful connection, ie:
#
#Connect /dev/serial0 source_system=255
#Log Directory: 
#Telemetry log: mav.tlog
#Waiting for heartbeat from /dev/serial0
#MAV> GPS lock at 1 meters
#Detected vehicle 1:1 on link 0
#online system 1
#STABILIZE> Mode STABILIZE
#AP: ArduCopter V4.0.3 (cc0ff08c)
#AP: ChibiOS: d4fce84e
#AP: hakrcminif4 0054002E 394E5005 20343942
#AP: RCOut: DS600:1-6
#AP: Frame: QUAD
# ...
#
# If this doesn't work, then mavlink-routerd won't work either.
# Debug: make sure that the appropriate "Serial" parameters on the FC have the same baud as below, and make sure using Mavlink protocol

mavproxy.py --master=/dev/serial0 --baud 921600
