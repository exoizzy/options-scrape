class Option:

    """
    includes copy constructor by setting opt=Option() object, otherwise all other fields must be filled
    """
    def __init__(self, contractTicker: str = None, strike: float = None, expDate: int = None, oi: int = None,
                 vol: int = None, iv: float = None, cop: str = None, underlying: str = None,
                 contractPrice: float = None, bid: float = None, ask: float = None, opt=None):
        if opt is None:
            self.contractTicker, self.strike, self.expDate, self.oi, self.vol, self.iv, self.cop, self.underlying, \
            self.contractPrice, self.bid, self.ask = contractTicker, strike, expDate, oi, vol, iv, cop, underlying, \
                                                     contractPrice, bid, ask
        else:
            self.contractTicker, self.strike, self.expDate, self.oi, self.vol, self.iv, self.cop, self.underlying, \
            self.contractPrice, self.bid, self.ask = opt.contractTicker, opt.strike, opt.expDate, opt.oi, opt.vol, \
                                                     opt.iv, opt.cop, opt.underlying, opt.contractPrice, opt.bid, \
                                                     opt.ask

    def __copy__(self):
        return Option(opt=self)

    def isCall(self):
        return self.cop == 'c'

    def isPut(self):
        return self.cop == 'p'

    def toRelative(self, maxOI, maxVol):
        self.oi = self.oi/maxOI
        self.vol = self.vol/maxVol
