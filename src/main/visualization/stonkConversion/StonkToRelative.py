from models import Stonk
from models import DaysOptions
import datetime

hid = 24
mih = 60


def getOIandVolFromStonk(stonk):
    pass


def stonkToRelativeXY(stonk: Stonk):
    pass


def daysOptionsToRelative(daysOpt: DaysOptions, tPrev):
    callOI, putOI, callVol, putVol = getOIandVolFromStonk(daysOpt)
    maxOI = max(callOI + putOI)
    maxVol = max(callVol + putVol)
    te = calcDeltaTMin(tPrev, daysOpt.expDate)

    relativeX(callOI, maxOI, te)
    relativeX(putOI, maxOI, te)
    relativeX(callVol, maxVol, te)
    relativeX(putVol, maxVol, te)


def calcDeltaTMin(tPrev: int, expiry: int):
    tp = datetime.date.fromtimestamp(tPrev)
    exp = datetime.date.fromtimestamp(expiry)
    rd = exp-tp

    return relativeDeltaToMin(rd)


def relativeDeltaToMin(timed: datetime.timedelta):
    return timed.days * hid * mih


def relativeX(rabArr, maxB, te):
    for i in range(0, len(rabArr)):
        rabArr[i] = (rabArr[i]/maxB)*te
