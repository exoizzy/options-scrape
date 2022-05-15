from interfaces.YahooFinance.YahooFinanceInterface import YahooFinanceInterface
from fileUtilities import FileUtility
import os
import src.res
import datetime
from dateutil.relativedelta import *

def main():
    # ticker = 'SPY'
    # yfi = YahooFinanceInterface(ticker)
    # stonk = yfi.get_stonk()
    #
    # if stonk is not None:
    #     FileUtility.saveStonkToJsonFile(stonk, 'first_try')
    # else:
    #     print('stonk is none :( \n')
    #

    x = {'1':1, '2':2, '3':3}
    dick(x)
    print(x)

    # t = 1450033030
    # t0 = datetime.date.fromtimestamp(t)
    # texp = datetime.date.today()
    # rd = texp-t0
    # print(rd.resolution)


def dick(y):
    for i in y.keys():
        y[i] = y[i]+1

    print(f'dicky: {y}')

if __name__ == '__main__':
    main()
