import ZeroBorg
import time
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
ZB.ResetEpo()

speed = 0.5

ZB.SetMotor1(speed)
time.sleep(5)
ZB.SetMotor2(speed)
time.sleep(5)
ZB.SetMotor3(speed)
time.sleep(5)
ZB.SetMotor4(speed)
time.sleep(5)

ZB.MotorsOff()