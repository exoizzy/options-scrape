from Option import Option


class Stonk:
    expDates: [int]
    options: [Option]
    maxOI: int
    maxVol: int

    def __init__(self, ticker, currentPrice, lastOpenDate, yrHigh=None, yrLow=None, dayHigh=None, dayLow=None):
        # current price == yfin.regularMarketPrice
        self.ticker, self.currentPrice, self.lastOpenDate, self.yrHigh, self.yrLow, self.dayHigh, self.dayLow = \
            ticker, currentPrice, lastOpenDate, yrHigh, yrLow, dayHigh, dayLow

