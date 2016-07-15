#!/usr/bin/env python
# coding: Latin-1

import ZeroBorg
import time









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
#failsafe = False
#for i in range(5):
#    ZB.SetCommsFailsafe(True)
#    failsafe = ZB.GetCommsFailsafe()
#    if failsafe:
#        break
#if not failsafe:
#    print 'Board %02X failed to report in failsafe mode!' % (ZB.i2cAddress)
#    sys.exit()
ZB.SetCommsFailsafe(False)
ZB.ResetEpo()



print ZB.GetCommsFailsafe()

#ZB.SetCommsFailsafe('disabled')
speed = 0.4
#ZB.SetMotor1(speed)
#time.sleep(5)
#ZB.SetMotor2(speed)
#time.sleep(5)
ZB.SetMotor3(speed)
time.sleep(10)
#ZB.SetMotor4(speed)
#time.sleep(5)

ZB.MotorsOff()
