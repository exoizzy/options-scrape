from models import Stonk
from models import DaysOptions
from models import Straddle
from models import Option
from models import RelativeModels
import datetime

hid = 8
mih = 60

"""
base function for converting Stonk object to an array of RelativeCoordinates for graphing
"""
def stonkToRelative(stonk: Stonk):
    relArr = []
    dopt = stonk.options
    tn = stonk.lastOpen
    relArr.append(daysOptionsToRelative(dopt[0], tn))

    for i in range(1, len(dopt)):
        tn = dopt[i-1].expDate
        relArr.append(daysOptionsToRelative(dopt[i], tn))

    return relArr


"""
converts DaysOptions object to dict's for call oi, put oi, call vol, and put vol
format: [{<strike>: <value>}]
"""
def getOIandVolFromDaysOpt(dopt: DaysOptions):
    straddles = dopt.straddles
    coi, poi, cvol, pvol = {}, {}, {}, {}
    for strad in straddles:
        strad: Straddle = strad
        c: Option = strad.call
        p: Option = strad.put
        strike: float = strad.strike
        if c is not None:
            coi.update(
                {strike: c.oi} # (c.oi if (p is None or p.oi > c.oi) else c.oi - p.oi)}
            )

            cvol.update(
                {strike: c.volume}
            )
        if p is not None:
            poi.update(
                {strike: p.oi} # (p.oi if (c is None or c.oi > p.oi) else p.oi - c.oi)}
            )
            pvol.update(
                {strike: p.volume}
            )

    return coi, poi, cvol, pvol


"""
converts stonk.options to RelativeCoordinates model
"""
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


"""
converts the two timestamps given for a days options to a time delta in minutes
"""
def calcDeltaTMin(tPrev: int, expiry: int):
    tp = datetime.date.fromtimestamp(tPrev)
    exp = datetime.date.fromtimestamp(expiry)
    rd = exp-tp

    return relativeDeltaToMin(rd)


"""
calculates the number of minutes (int) in the given timedelta.days
using minutes since that is the 'finest' setting available in most charting
"""
def relativeDeltaToMin(timed: datetime.timedelta):
    return timed.days * hid * mih


"""
converts vol/oi value to %(float) value based on the max of that days data set
te is used to denote the time delta to be used when charting, currently not being used due to plotly implementation
"""
def relativeX(rabArr, maxB, te):
    for i in rabArr.keys():
        rabArr[i] = rabArr[i]/maxB # *(-te)
