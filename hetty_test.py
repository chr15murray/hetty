#!/usr/bin/env python
# coding: Latin-1

import serial
import time
from xbee import XBee, ZigBee
import ZeroBorg

leftstick_assignments = {'button': 'dio-4', 'x': 'adc-0', 'y': 'adc-1'}
rightstick_assignments = {'button': 'dio-5', 'x': 'adc-2', 'y': 'adc-3'}

leftstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmax': 1023, 'ymin': 0, 'ymax': 1023}
rightstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmax': 1023, 'ymin': 0, 'ymax': 1023}

axis_nullzone = 200

controllerupdate = False

# Functions
def controller_callback(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    """
    global leftstick
    global rightstick
    global controllerupdate
    global axis_nullzone

    #  Uncomment for debug controller data
    #  print data

    # Temp storage for new values
    triggerupdate = False
    newleftstick = {}
    newrightstick = {}

    # Left Stick Button Handling
    newleftstick['button'] = not bool(data['samples'][0][leftstick_assignments['button']])
    if newleftstick['button'] != leftstick['button']:
        leftstick['button'] = newleftstick['button']
        triggerupdate = True

    # Right Stick Button Handling
    newrightstick['button'] = not bool(data['samples'][0][rightstick_assignments['button']])
    if newrightstick['button'] != rightstick['button']:
        rightstick['button'] = newrightstick['button']
        triggerupdate = True

    # Left X-Axis Handling
    newleftstick['x'] = int(data['samples'][0][leftstick_assignments['x']])
    if newleftstick['x'] < leftstick['x'] -axis_nullzone or leftstick['x'] + axis_nullzone < newleftstick['x']:
        leftstick['x'] = newleftstick['x']
        triggerupdate = True

    # Left Y-Axis Handling
    newleftstick['y'] = int(data['samples'][0][leftstick_assignments['y']])
    if newleftstick['y'] < leftstick['y'] -axis_nullzone or leftstick['y'] + axis_nullzone < newleftstick['y']:
        leftstick['y'] = newleftstick['y']
        triggerupdate = True

    # Right X-Axis Handling
    newrightstick['x'] = int(data['samples'][0][rightstick_assignments['x']])
    if newrightstick['x'] < rightstick['x'] -axis_nullzone or rightstick['x'] + axis_nullzone < newrightstick['x']:
        rightstick['x'] = newrightstick['x']
        triggerupdate = True

    # Right Y-Axis Handling
    newrightstick['y'] = int(data['samples'][0][rightstick_assignments['y']])
    if newrightstick['y'] < rightstick['y'] -axis_nullzone or rightstick['y'] + axis_nullzone < newrightstick['y']:
        rightstick['y'] = newrightstick['y']
        triggerupdate = True


    # If any updates have been made set this flag to ensure they are processed
    if triggerupdate:
        controllerupdate = True



# Setup the Xbee
serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = ZigBee(serial_port, callback=controller_callback)


# Setup the ZeroBorg
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
if not ZB.foundChip:
    boards = ZeroBorg.ScanForZeroBorg()
    if len(boards) == 0:
        print 'No ZeroBorg found, check you are attached :)'
    else:
        print 'No ZeroBorg at address %02X, but we did find boards:' % (ZB.i2cAddress)
        for board in boards:
            print '    %02X (%d)' % (board, board)
        print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
        print 'ZB.i2cAddress = 0x%02X' % (boards[0])
    sys.exit()
#ZB.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
# Ensure the communications failsafe has been enabled!
failsafe = False
for i in range(5):
    ZB.SetCommsFailsafe(True)
    failsafe = ZB.GetCommsFailsafe()
    if failsafe:
        break
if not failsafe:
    print 'Board %02X failed to report in failsafe mode!' % (ZB.i2cAddress)
    sys.exit()
ZB.ResetEpo()



while True:
    if controllerupdate == True:
        #print leftstick
        #print rightstick

        # Speed + is anti-clockwise
        # Speed - in clockwise

        # Forward
        if leftstick['x'] < 511 - axis_nullzone:
             speed = 0.5
             ZB.SetMotor1(-speed)   # Front Right
             ZB.SetMotor2(-speed)   # Back Right
             ZB.SetMotor3(speed)    # Back Left
             ZB.SetMotor4(speed)    # Front Left
        # Reverse
        elif leftstick['x'] > 511 + axis_nullzone:
            speed = 0.5
            ZB.SetMotor1(speed)  # Front Right
            ZB.SetMotor2(speed)  # Back Right
            ZB.SetMotor3(-speed)  # Back Left
            ZB.SetMotor4(-speed)  # Front Left
        # Left
        elif leftstick['y'] < 511 - axis_nullzone:
            speed = 0.5
            ZB.SetMotor1(-speed)  # Front Right
            ZB.SetMotor2(speed)  # Back Right
            ZB.SetMotor3(speed)  # Back Left
            ZB.SetMotor4(-speed)  # Front Left
        # Right
        elif leftstick['y'] > 511 + axis_nullzone:
            speed = 0.5
            ZB.SetMotor1(speed)  # Front Right
            ZB.SetMotor2(-speed)  # Back Right
            ZB.SetMotor3(-speed)  # Back Left
            ZB.SetMotor4(speed)  # Front Left
        # Spin Left
        elif rightstick['y'] < 511 - axis_nullzone:
            speed = 0.5
            ZB.SetMotor1(-speed)  # Front Right
            ZB.SetMotor2(-speed)  # Back Right
            ZB.SetMotor3(-speed)  # Back Left
            ZB.SetMotor4(-speed)  # Front Left
        # Spin Right
        elif rightstick['y'] > 511 + axis_nullzone:
            speed = 0.5
            ZB.SetMotor1(speed)  # Front Right
            ZB.SetMotor2(speed)  # Back Right
            ZB.SetMotor3(speed)  # Back Left
            ZB.SetMotor4(speed)  # Front Left
        else:
             ZB.MotorsOff()

        # Reset ControllerUpdate Variable
        controllerupdate = False

#    try:
#        time.sleep(0.001)
#    except KeyboardInterrupt:
#        break

xbee.halt()
serial_port.close()
