import models.RelativeModels
from interfaces.YahooFinance.YahooFinanceInterface import YahooFinanceInterface
from fileUtilities import FileUtility
from visualization.stonkConversion import StonkToRelative
from models.RelativeModels import RelativeCoordinates
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
    title = f'{ticker} oi and vol graph'
    xaxTitle = 'vol && oi (value/max as % of time to expiry)'
    yaxTitle = 'strike price ($)'
    fn = 'SPY_2022-05-23_test-2022-05-23_stonk.json'

    # yfi = YahooFinanceInterface(ticker)
    # stonk = yfi.get_stonk()
    # if stonk is not None:
    #     fn = FileUtility.saveStonkToJsonFile(stonk, f'test-{datetime.date.today()}')
    # else:
    #     print('stonk is none :( \n')

    if fn is not None:
        ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)

        rel = StonkToRelative.daysOptionsToRelative(ftstonk.options[0], ftstonk.lastOpen)
        pli = PlotlyInterface(ftstonk.ticker, title, xaxTitle, yaxTitle)

        plotRelativeModel(rel, pli, ftstonk.currentPrice, 'v')

        pli.showGraph(ftstonk.currentPrice)


def plotRelativeModel(rel: RelativeCoordinates, pli: PlotlyInterface, cprice: float, ori):
    cvx = list(rel.callVol.values())
    cvy = list(rel.callVol.keys())
    pvx = list(rel.putVol.values())
    pvy = list(rel.putVol.keys())
    cox = list(rel.callOI.values())
    coy = list(rel.callOI.keys())
    pox = list(rel.putOI.values())
    poy = list(rel.putOI.keys())

    print(f'len cvx: {len(cox)}, len cvy: {len(coy)}')
    print(f'len pox: {len(pox)}, len poy: {len(poy)}')

    if ori == 'v':
        pli.orientation = ori
        pli.addLine(cvy, cvx, pli.red, 'callVol')
        pli.addLine(pvy, pvx, pli.blue, 'putVol')
        pli.addBar(coy, cox, pli.red, 'callOI')
        pli.addBar(poy, pox, pli.blue, 'putOI')

        pli.addNextBar(coy, cox, 'pink', 'testC')
        pli.addNextBar(poy, pox, 'yellow', 'testP')
    elif ori == 'h':
        pli.addLine(cvx, cvy, pli.red, 'callVol')
        pli.addLine(pvx, pvy, pli.blue, 'putVol')
        pli.addBar(cox, coy, pli.red, 'callOI')
        pli.addBar(pox, poy, pli.blue, 'putOI')

    # pli.showGraph(cprice)


if __name__ == '__main__':
    main()
