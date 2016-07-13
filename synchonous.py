import serial
from xbee import XBee, ZigBee

serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = ZigBee(serial_port)

while True:
    try:
        controller = xbee.wait_read_frame()
	print controller

    except KeyboardInterrupt:
        break

serial_port.close()
