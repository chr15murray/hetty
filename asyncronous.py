import serial
import time
from xbee import XBee, ZigBee

serial_port = serial.Serial('/dev/ttyAMA0', 9600)

def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    """
    print data

#xbee = XBee(serial_port, callback=print_data)
xbee = ZigBee(serial_port, callback=print_data)

while True:
    try:
	print testprint
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()
