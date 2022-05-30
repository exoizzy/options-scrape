from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import timezone

from models import Stonk, Option

hid = 8
mih = 60


def stonkToXY(stonk: Stonk):
    """

    :param stonk:
    :return:
    """




def calcDeltaTMin(tPrev: int, expiry: int):
    """
    converts the two timestamps given for a days options to a time delta in minutes
    :param tPrev: previous expiry/market close
    :param expiry: contract's expiry
    :return: time to previous expiry/mkt close in minutes
    """
    tp = date.fromtimestamp(tPrev)
    exp = date.fromtimestamp(expiry)
    rd = exp-tp

    return relativeDeltaToMin(rd)


def relativeDeltaToMin(timed: timedelta):
    """
    calculates the number of minutes (int) in the given timedelta.days
    using minutes since that is the 'finest' setting available in most charting
    :param timed: timedelta
    :return: calculates the number of minutes (int) in the given timedelta.days
    """
    return timed.days * hid * mih


def relativeX(rabArr, maxB, te):
    """
    converts vol/oi value to %(float) value based on the max of that days data set
    :param rabArr:
    :param maxB:
    :param te: used to denote the time delta to be used when charting, currently not being used due to plotly implementation
    :return:
    """
    for i in rabArr.keys():
        rabArr[i] = rabArr[i]/maxB *(-te)
