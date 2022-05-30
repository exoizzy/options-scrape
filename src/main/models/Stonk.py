from json import JSONEncoder

from models import Option


class Stonk:
    expDates: [int]
    strikes: [int]
    options: [Option]
    maxOI: int
    maxVol: int

    """
    includes copy constructor by setting stnk=Stonk() object
    otherwise all other values must be set
    """
    def __init__(self, ticker: str = None, currentPrice: float = None, lastOpenDate: int = None, yrHigh: float = None, yrLow: float = None,
                 dayHigh: float = None, dayLow: float = None, stnk=None):
        if stnk is None:
            self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow = \
                ticker, currentPrice, lastOpenDate, yrHigh, yrLow, dayHigh, dayLow
        else:
            self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow = \
            stnk.ticker, stnk.currentPrice, stnk.lastOpenDate, stnk.yrHigh, stnk.yrLow, stnk.dayHigh, stnk.dayLow

            self.expDates, self.strikes, self.options, self.maxOI, self.maxVol = \
            stnk.expDates, stnk.strikes, stnk.options.deepcopy(), stnk.maxOI, stnk.maxVol

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