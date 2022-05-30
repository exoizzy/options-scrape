class Option:

    def __init__(self, contractTicker: str, strike: float, expDate: int, oi: int, vol: int, iv: float, cop: str,
                 underlying: str, contractPrice: float, bid: float = None, ask: float = None):
        self.contractTicker, self.strike, self.expDate, self.oi, self.vol, self.iv, self.cop, self.underlying, \
        self.contractPrice, self.bid, self.ask = contractTicker, strike, expDate, oi, vol, iv, cop, underlying, \
                                                 contractPrice, bid, ask

    def isCall(self):
        return self.cop == 'c'

    def isPut(self):
        return self.cop == 'p'
