from json import JSONEncoder

from models import Option


class Stonk:
    expDates: [int]
    strikes: [int]
    options: [Option]
    maxOI: int
    maxVol: int

    def __init__(self, ticker: str = None, currentPrice: float = None, lastOpenDate: int = None, yrHigh: float = None, yrLow: float = None,
                 dayHigh: float = None, dayLow: float = None):
        self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow = \
            ticker, currentPrice, lastOpenDate, yrHigh, yrLow, dayHigh, dayLow

    def __copy__(self):
        cpy = Stonk(self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow)
        cpy.maxVol = self.maxVol
        cpy.maxOI = self.maxOI
        cpy.expDates = self.expDates.copy()
        cpy.strikes = self.strikes.copy()
        cpy.options = []
        for o in self.options:
            o: Option = o
            cpy.options.append(o.__copy__())
        return cpy

    def getAllOIAndVol(self):
        oi, vol = [], []

        for opt in self.options:
            opt: Option = opt
            oi.append(opt.oi)
            vol.append(opt.vol)

        return oi, vol

    def calcMaxOIAndVol(self):
        if len(self.options) != 0:
            oi, vol = self.getAllOIAndVol()
            self.maxOI = max(oi)
            self.maxVol = max(vol)

    def toRelative(self):
        if self.maxVol is not None and self.maxOI is not None:
            pass


class StonkEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
