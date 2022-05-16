from models import Stonk
from models import DaysOptions
from models import Straddle
from models import Option
from models import RelativeModels
import datetime

hid = 24
mih = 60


def getOIandVolFromDaysOpt(dopt: DaysOptions):
    straddles = dopt.straddles
    coi, poi, cvol, pvol = {}, {}, {}, {}
    for strad in straddles:
        strad: Straddle = strad
        c: Option = strad.call
        p: Option = strad.put
        strike: float = strad.strike
        coi.update(
            {strike: c.oi}
        )
        poi.update(
            {strike: p.oi}
        )
        cvol.update(
            {strike: c.volume}
        )
        pvol.update(
            {strike: p.volume}
        )

    return coi, poi, cvol, pvol


def daysOptionsToRelative(daysOpt: DaysOptions, tPrev):
    # { strike: <oi/vol> }
    callOI: dict
    putOI: dict
    callVol: dict
    putVol: dict
    callOI, putOI, callVol, putVol = getOIandVolFromDaysOpt(daysOpt)
    maxOI = max(list(callOI.values()) + list(putOI.values()))
    maxVol = max(list(callVol.values()) + list(putVol.values()))
    te = calcDeltaTMin(tPrev, daysOpt.expDate)

    relativeX(callOI, maxOI, te)
    relativeX(putOI, maxOI, te)
    relativeX(callVol, maxVol, te)
    relativeX(putVol, maxVol, te)

    return RelativeModels.RelativeCoordinates(daysOpt.expDate, tPrev, maxOI, maxVol, callOI, putOI, callVol, putVol)


def calcDeltaTMin(tPrev: int, expiry: int):
    tp = datetime.date.fromtimestamp(tPrev)
    exp = datetime.date.fromtimestamp(expiry)
    rd = exp-tp

    return relativeDeltaToMin(rd)


def relativeDeltaToMin(timed: datetime.timedelta):
    return timed.days * hid * mih


def relativeX(rabArr, maxB, te):
    for i in rabArr.keys():
        rabArr[i] = (rabArr[i]/maxB)*te
