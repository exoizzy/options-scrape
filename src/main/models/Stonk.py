from datetime import date
from models import Straddle
from json import JSONEncoder


class Stonk:
    ticker: str
    currentPrice: float
    options: {date: [Straddle]}
    expDates: [date]
    lastOpen: int

    def __init__(self, ticker, currentPrice, options, expDates, lastopen):
        self.ticker = ticker
        self.currentPrice = currentPrice
        self.options = options
        self.expDates = expDates
        self.lastOpen = lastopen


class StonkEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__