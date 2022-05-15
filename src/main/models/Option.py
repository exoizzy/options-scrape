from datetime import date


class OptDate:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day


class Option:
    contractTicker: str
    underlyingTicker: str
    expDate: date
    callOrPut: str
    strike: int
    volume: int
    oi: int
    iv: float
    contractPrice: float
    optDate: OptDate

    def __init__(self, contractTicker, underlyingTicker, expDate, cop, strike, vol, oi, iv, contractPrice, optDate):
        self.contractTicker = contractTicker
        self.underlyingTicker = underlyingTicker
        self.expDate = expDate
        self.callOrPut = cop
        self.strike = strike
        self.volume = vol
        self.oi = oi
        self.iv = iv
        self.contractPrice = contractPrice
        self.optDate = optDate
