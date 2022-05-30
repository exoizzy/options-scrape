from Option import Option


class Stonk:
    expDates: [int]
    strikes: [int]
    options: [Option]
    maxOI: int
    maxVol: int

    def __init__(self, ticker: str, currentPrice: float, lastOpenDate: int, yrHigh: float = None, yrLow: float = None,
                 dayHigh: float = None, dayLow: float = None):
        # current price == yfin.regularMarketPrice
        self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow = \
            ticker, currentPrice, lastOpenDate, yrHigh, yrLow, dayHigh, dayLow

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
