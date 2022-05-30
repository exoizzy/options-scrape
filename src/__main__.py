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
from models.Straddle import DaysOptions, Straddle
from models.RelativeModels import RelativeCoordinates
from visualization.plotlyInterface.PlotlyInterface import PlotlyInterface
from visualization.stonkConversion import StonkToRelative


def main():
    ticker = 'CRM'
    title = f'{ticker} oi and vol graph'
    xaxTitle = 'vol && oi (value/max as % of time to expiry)'
    yaxTitle = 'strike price ($)'
    fn = 'CRM_2022-05-29_test_stonk.json'
    gfn = f''

    if False:
        yfi = YahooFinanceInterface(ticker)
        stonk = yfi.get_stonk()
        if stonk is not None:
            fn = FileUtility.saveStonkToJsonFile(stonk, f'test')
        else:
            print('stonk is none :( \n')

            # todo: need to figure out a way to not create an oi bar if the value is 0 for both.

    if fn is not None:
        ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)
        pli = PlotlyInterface(ftstonk.ticker, title, xaxTitle, yaxTitle)

        plotStonk(ftstonk, pli, 'h')
        FileUtility.saveGraphHtml(pli.fig.to_html(), ticker, f'test-save')


def plotStonk(stonk: Stonk, pli: PlotlyInterface, orientation: str):
    tickArr = []
    tickVals = []
    relArr = StonkToRelative.stonkToRelative(stonk)

    for i in range(0, len(relArr)):
        tickVals.append(i)
        tickArr.append(str(datetime.date.fromtimestamp(relArr[i].expiry)))
        plotRelativeModel(relArr[i], pli, orientation, i)
        # mp = calcMaxPain(stonk.currentPrice, stonk.options[i])
        # if orientation == 'h':
        #     pli.addBar([1], [mp], 'black', 'mp', i)

    pli.fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=tickVals,
            ticktext=tickArr
        )
    )
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
        pli.addBar(coy, cox, pli.red, 'callOI', offset)
        pli.addBar(poy, pox, pli.blue, 'putOI', offset)
        pli.addLine(cvy, cvx, pli.red, 'callVol', offset)
        pli.addLine(pvy, pvx, pli.blue, 'putVol', offset)

    elif ori == 'h':
        pli.addLine(cvx, cvy, pli.red, 'callVol', offset)
        pli.addLine(pvx, pvy, pli.blue, 'putVol', offset)
        pli.addBar(cox, coy, pli.red, 'callOI', offset)
        pli.addBar(pox, poy, pli.blue, 'putOI', offset)


def calcMaxPain(curprice, dopt: DaysOptions):
    mp = {}

    for st in dopt.straddles:
        st: Straddle = st
        dif = abs(curprice - st.strike)
        cval = st.call.oi * st.call.contractPrice
        pval = st.put.oi * st.put.contractPrice
        val = dif * (cval + pval)
        mp.update({st.strike: val})

    vals = list(mp.values())
    keys = list(mp.keys())
    ind = vals.index(max(vals))

    return keys[ind]


if __name__ == '__main__':
    main()
