

class Option:

    def __init__(self, contractTicker, expDate, oi, vol, iv, cop, underlying, bid=None, ask=None):
        self.contractTicker, self.expDate, self.oi, self.vol, self.iv, self.cop, self.underlying, self.bid, self.ask \
            = contractTicker, expDate, oi, vol, iv, cop, underlying, bid, ask

    def isCall(self):
        return self.cop == 'c'

    def isPut(self):
        return self.cop == 'p'
