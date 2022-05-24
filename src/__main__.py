import os
import datetime
from dateutil.relativedelta import *
import plotly.express as px
import plotly.graph_objects as go
import src.res
from fileUtilities import FileUtility
from interfaces.YahooFinance.YahooFinanceInterface import YahooFinanceInterface
import models.RelativeModels
from models import Stonk
from models.Straddle import DaysOptions
from models.RelativeModels import RelativeCoordinates
from visualization.plotlyInterface.PlotlyInterface import PlotlyInterface
from visualization.stonkConversion import StonkToRelative


def main():
    ticker = 'SPY'
    title = f'{ticker} oi and vol graph'
    xaxTitle = 'vol && oi (value/max as % of time to expiry)'
    yaxTitle = 'strike price ($)'
    fn = 'SPY_2022-05-24_test-2022-05-24_stonk.json'

    # yfi = YahooFinanceInterface(ticker)
    # stonk = yfi.get_stonk()
    # if stonk is not None:
    #     fn = FileUtility.saveStonkToJsonFile(stonk, f'test')
    # else:
    #     print('stonk is none :( \n')

    if fn is not None:
        ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)
        pli = PlotlyInterface(ftstonk.ticker, title, xaxTitle, yaxTitle)

        plotStonk(ftstonk, pli, 'h')


def plotStonk(stonk: Stonk, pli: PlotlyInterface, orientation: str):
    relArr = StonkToRelative.stonkToRelative(stonk)

    for i in range(0, len(relArr)):
        plotRelativeModel(relArr[i], pli, orientation, i)

    pli.showGraph(stonk.currentPrice)

def plotRelativeModel(rel: RelativeCoordinates, pli: PlotlyInterface, ori, offset):
    cvx = list(rel.callVol.values())
    cvy = list(rel.callVol.keys())
    pvx = list(rel.putVol.values())
    pvy = list(rel.putVol.keys())
    cox = list(rel.callOI.values())
    coy = list(rel.callOI.keys())
    pox = list(rel.putOI.values())
    poy = list(rel.putOI.keys())

    # print(f'len cvx: {len(cox)}, len cvy: {len(coy)}')
    # print(f'len pox: {len(pox)}, len poy: {len(poy)}')

    if ori == 'v':
        pli.orientation = ori
        pli.addLine(cvy, cvx, pli.red, 'callVol', offset)
        pli.addLine(pvy, pvx, pli.blue, 'putVol', offset)
        pli.addBar(coy, cox, pli.red, 'callOI', offset)
        pli.addBar(poy, pox, pli.blue, 'putOI', offset)

    elif ori == 'h':
        pli.addLine(cvx, cvy, pli.red, 'callVol', offset)
        pli.addLine(pvx, pvy, pli.blue, 'putVol', offset)
        pli.addBar(cox, coy, pli.red, 'callOI', offset)
        pli.addBar(pox, poy, pli.blue, 'putOI', offset)



if __name__ == '__main__':
    main()
