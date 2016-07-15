#!/usr/bin/env python
# coding: Latin-1

import serial
import time
from xbee import ZigBee
import ZeroBorg
import math

leftstick_assignments = {'button': 'dio-4', 'x': 'adc-0', 'y': 'adc-1'}
rightstick_assignments = {'button': 'dio-5', 'x': 'adc-2', 'y': 'adc-3'}

leftstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
rightstick = {'button': False, 'x': 511, 'y': 511, 'xmin': 0, 'xmid': 511, 'xmax': 1023, 'ymin': 0, 'ymid': 511, 'ymax': 1023}
controllermovement = {'degree': 0, 'speed': 0, 'rotation': 0}
calibrationdata = {'samples': 10, 'samplestaken': 0, 'leftxmid': {0: 0}, 'leftymid': {0: 0}, 'rightxmid': {0: 0}, 'rightymid': {0: 0}}
axis_nullzone = 200
calibrationmode = False

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
    global controllermovement
    global axis_nullzone
    global calibrationmode
    global calibrationdata

    #  Uncomment for debug controller data
    #print data

    # Calibration mode
    if calibrationmode:
        if calibrationdata['samplestaken'] < calibrationdata['samples']:
            i = calibrationdata['samplestaken']
            calibrationdata['leftxmid'][i] = int(data['samples'][0][leftstick_assignments['x']])
            calibrationdata['leftymid'][i] = int(data['samples'][0][leftstick_assignments['y']])
            calibrationdata['rightxmid'][i] = int(data['samples'][0][rightstick_assignments['x']])
            calibrationdata['rightymid'][i] = int(data['samples'][0][rightstick_assignments['y']])
            calibrationdata['samplestaken'] = calibrationdata['samplestaken'] + 1
        else:
            calibrationmode = False
            calibrationdata['samplestaken'] = 0
            leftstick['xmid'] = sum(calibrationdata['leftxmid'].values()) / len(calibrationdata['leftxmid'])
            leftstick['ymid'] = sum(calibrationdata['leftymid'].values()) / len(calibrationdata['leftymid'])
            rightstick['xmid'] = sum(calibrationdata['rightxmid'].values()) / len(calibrationdata['rightxmid'])
            rightstick['ymid'] = sum(calibrationdata['rightymid'].values()) / len(calibrationdata['rightymid'])
        return

    # Basic stick values
    leftstick['button'] = not bool(data['samples'][0][leftstick_assignments['button']])
    rightstick['button'] = not bool(data['samples'][0][rightstick_assignments['button']])
    leftstick['x'] = int(data['samples'][0][leftstick_assignments['x']])
    leftstick['y'] = int(data['samples'][0][leftstick_assignments['y']])
    rightstick['x'] = int(data['samples'][0][rightstick_assignments['x']])
    rightstick['y'] = int(data['samples'][0][rightstick_assignments['y']])


def calibratejoysticks():
    global calibrationmode

    calibrationmode = True
    print('Calibrating Joysticks - Please do not touch')

    while calibrationmode:
        time.sleep(1)

    print('calibration complete')
    print('Left Stick - X Axis - Mid point: ' + str(leftstick['xmid']))
    print('Left Stick - Y Axis - Mid point: ' + str(leftstick['ymid']))
    print('Right Stick - X Axis - Mid point: ' + str(rightstick['xmid']))
    print('Right Stick - Y Axis - Mid point: ' + str(rightstick['ymid']))
    return

def calc_controller_movement(stick):
    movement = {}

    # Stick X range and position
    if stick['x'] >= stick['xmid']:
        stickxrange = float(stick['xmax'] - stick['xmid'])
        stickxpos = float(stick['x'] - stick['xmid'])
    else:
        stickxrange = float(stick['xmid'] - stick['xmin'])
        stickxpos = float(stick['xmid'] - stick['x'])

    # Stick Y range and position
    if stick['y'] >= stick['ymid']:
        stickyrange = float(stick['ymax'] - stick['ymid'])
        stickypos = float(stick['y'] - stick['ymid'])
    else:
        stickyrange = float(stick['ymid'] - stick['ymin'])
        stickypos = float(stick['ymid'] - stick['y'])

    # Convert position to relative position
    relx = 100 * stickxpos / stickxrange
    rely = 100 * stickypos / stickyrange

    movement['speed'] = -1

    if stick['x'] >= stick['xmid'] and stick['y'] >= stick['ymid']:
        # Handle 0 co-ordinates
        if stickxpos == stickypos == 0:
            movement['degree'] = 360
            movement['speed'] = 0
        elif stickxpos == 0:
            movement['degree'] = 360
            movement['speed'] = 100 * stickypos / stickyrange
        elif stickypos == 0:
            movement['degree'] = 90
            movement['speed'] = 100 * stickxpos / stickxrange
        else:
            movement['degree'] = round(math.degrees(math.atan2(relx, rely)))


    elif stick['x'] >= stick['xmid'] and stick['y'] < stick['ymid']:
        # 90 to 180 degree
        movement['degree'] = 90 + round(math.degrees(math.atan2(rely, relx)))

    elif stick['x'] < stick['xmid'] and stick['y'] < stick['ymid']:
        # 180 to 270 degree
        movement['degree'] = 180 + round(math.degrees(math.atan2(relx, rely)))

    else:
        # 270 to 360 degree
        movement['degree'] = 270 + round(math.degrees(math.atan2(rely, relx)))

    # Calculate speed for most cases
    if movement['speed'] == -1:
        spos = round(math.hypot(rely, relx))
        movement['speed'] = round(spos / 1.41421356237)  # 100 * math.hypot(100, 100))
    return movement




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

# Calibrate the joysticks
calibratejoysticks()


while True:
    try:

        # Speed + is anti-clockwise
        # Speed - in clockwise

        movement = calc_controller_movement(leftstick)
        speed = movement['speed'] / 100

        if speed < 20:
            speed = 0

        # Forward
        #if leftstick['x'] < leftstick['xmid'] - axis_nullzone:
        if 315 < movement['degree'] or movement['degree'] < 45:
             #speed = 0.5
             ZB.SetMotor1(-speed)   # Front Right
             ZB.SetMotor2(-speed)   # Back Right
             ZB.SetMotor3(speed)    # Back Left
             ZB.SetMotor4(speed)    # Front Left
        # Reverse
        #elif leftstick['x'] > leftstick['xmid'] + axis_nullzone:
        elif 135 < movement['degree'] < 225:
            #speed = 0.5
            ZB.SetMotor1(speed)  # Front Right
            ZB.SetMotor2(speed)  # Back Right
            ZB.SetMotor3(-speed)  # Back Left
            ZB.SetMotor4(-speed)  # Front Left
        # Left
        #elif leftstick['y'] < leftstick['ymid'] - axis_nullzone:
        elif 225 < movement['degree'] < 315:
            speed = 0.5
            ZB.SetMotor1(-speed)  # Front Right
            ZB.SetMotor2(speed)  # Back Right
            ZB.SetMotor3(speed)  # Back Left
            ZB.SetMotor4(-speed)  # Front Left
        # Right
        #elif leftstick['y'] > leftstick['ymid'] + axis_nullzone:
        elif 45 < movement['degree'] < 135:
            speed = 0.5
            ZB.SetMotor1(speed)  # Front Right
            ZB.SetMotor2(-speed)  # Back Right
            ZB.SetMotor3(-speed)  # Back Left
            ZB.SetMotor4(speed)  # Front Left
        # Spin Left
#        elif rightstick['y'] < rightstick['ymid'] - axis_nullzone:
#            speed = 0.5
#            ZB.SetMotor1(-speed)  # Front Right
#            ZB.SetMotor2(-speed)  # Back Right
#            ZB.SetMotor3(-speed)  # Back Left
#            ZB.SetMotor4(-speed)  # Front Left
        # Spin Right
#        elif rightstick['y'] > rightstick['ymid'] + axis_nullzone:
#            speed = 0.5
#            ZB.SetMotor1(speed)  # Front Right
#            ZB.SetMotor2(speed)  # Back Right
#            ZB.SetMotor3(speed)  # Back Left
#            ZB.SetMotor4(speed)  # Front Left
        else:
             ZB.MotorsOff()

        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()
