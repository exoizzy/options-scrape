from interfaces.YahooFinance.YahooFinanceInterface import YahooFinanceInterface
from fileUtilities import FileUtility
from visualization.stonkConversion import StonkToRelative
import os
import src.res
import datetime
from dateutil.relativedelta import *
import plotly.express as px
import plotly.graph_objects as go

from models import Stonk


def main():
    ticker = 'SPY'
    yfi = YahooFinanceInterface(ticker)
    stonk = yfi.get_stonk()

    if stonk is not None:
        filename = FileUtility.saveStonkToJsonFile(stonk, 'test-05202022')

        ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, filename)

        rel = StonkToRelative.daysOptionsToRelative(ftstonk.options[0], ftstonk.lastOpen)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=list(rel.callVol.keys()), y=list(rel.callVol.values()),
                       mode='lines',
                       name='callVol')
        )
        fig.add_trace(
            go.Scatter(x=list(rel.putVol.keys()), y=list(rel.putVol.values()),
                       mode='lines',
                       name='putVol')
        )

        fig.show()
    else:
        print('stonk is none :( \n')


    # x = {'1':1, '2':2, '3':3}
    # dick(x)
    # print(x.values())

    # t = 1450033030
    # t0 = datetime.date.fromtimestamp(t)
    # texp = datetime.date.today()
    # rd = texp-t0
    # print(rd.resolution)


def dick(y):
    for i in y.keys():
        y[i] = y[i] + 1

    print(f'dicky: {y}')

if __name__ == '__main__':
    main()
