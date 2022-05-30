class Option:

    """
    includes copy constructor by setting opt=Option() object, otherwise all other fields must be filled
    """
    def __init__(self, contractTicker: str = None, strike: float = None, expDate: int = None, oi: int = None,
                 vol: int = None, iv: float = None, cop: str = None, underlying: str = None,
                 contractPrice: float = None, bid: float = None, ask: float = None, *args, **kwargs):
        self.contractTicker, self.strike, self.expDate, self.oi, self.vol, self.iv, self.cop, self.underlying, \
        self.contractPrice, self.bid, self.ask = contractTicker, strike, expDate, oi, vol, iv, cop, underlying, \
                                                 contractPrice, bid, ask

    # todo: figure this shit out cause im fucking annoyed rn and need to eat
    # def __copy__(self):
    #     return Option(self)

    def isCall(self):
        return self.cop == 'c'

    def isPut(self):
        return self.cop == 'p'

    def toRelative(self, maxOI, maxVol):
        self.oi = self.oi/maxOI
        self.vol = self.vol/maxVol
