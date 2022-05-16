from datetime import date
from models import Option


class Straddle:
    strike: float
    expDate: date
    call: Option
    put: Option

    def __init__(self, strike, expDate, call, put):
        self.strike = strike
        self.expDate = expDate
        self.call = call
        self.put = put


class DaysOptions:
    def __init__(self, expDate: int, straddles: [Straddle]):
        self.expDate, self.straddles = expDate, straddles
