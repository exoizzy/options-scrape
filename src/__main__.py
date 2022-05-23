from interfaces.YahooFinance.YahooFinanceInterface import YahooFinanceInterface
from fileUtilities import FileUtility
from visualization.stonkConversion import StonkToRelative
from visualization.plotlyInterface.PlotlyInterface import PlotlyInterface
import os
import src.res
import datetime
from dateutil.relativedelta import *
import plotly.express as px
import plotly.graph_objects as go

from models import Stonk


def main():
    ticker = 'SPY'
    title = 'relative with old oi calcs'
    xaxTitle = 'vol && oi (value/max as % of time to expiry)'
    yaxTitle = 'strike price ($)'
    fn = 'SPY_2022-05-23_test-2022-05-23_stonk.json'
    # yfi = YahooFinanceInterface(ticker)
    # stonk = yfi.get_stonk()
    #
    # if stonk is not None:
    #     fn = FileUtility.saveStonkToJsonFile(stonk, f'test-{datetime.date.today()}')
    # else:
    #     print('stonk is none :( \n')

    if fn is not None:
        ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)

        rel = StonkToRelative.daysOptionsToRelative(ftstonk.options[0], ftstonk.lastOpen)

        pli = PlotlyInterface(ftstonk.ticker, title, xaxTitle, yaxTitle)

        pli.addLine(list(rel.callVol.values()), list(rel.callVol.keys()), pli.red, 'callVol')
        pli.addLine(list(rel.putVol.values()), list(rel.putVol.keys()), pli.blue, 'putVol')
        pli.addBar(list(rel.callOI.values()), list(rel.callOI.keys()), pli.red, 'callOI')
        pli.addBar(list(rel.putOI.values()), list(rel.putOI.keys()), pli.blue, 'putOI')

        pli.showGraph()

if __name__ == '__main__':
    main()
