import ZeroBorg
import time
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
ZB.ResetEpo()

while True:
    if ZB.HasNewIrMessage():
        ZB.GetIrMessage()
