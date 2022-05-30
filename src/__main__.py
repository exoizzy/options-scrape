import datetime

from fileUtilities import FileUtility
from interfaces.YahooFinance import YahooFinanceInterface
from models import Stonk, Option
from models.RelativeModels import RelativeCoordinates
from visualization.plotlyInterface import PlotlyInterface


def main():
    ticker = 'SPY'
    title = f'{ticker} oi and vol graph'
    xaxTitle = 'vol && oi (value/max as % of time to expiry)'
    yaxTitle = 'strike price ($)'
    fn = 'SPY_2022-05-30_new-format-test_stonk.json'

    if False:
        yfi = YahooFinanceInterface(ticker, 5)
        stonk = yfi.get_stonk()
        if stonk is not None:
            fn = FileUtility.saveStonkToJsonFile(stonk, f'new-format-test')
        else:
            print('stonk is none :( \n')

            # todo: need to figure out a way to not create an oi bar if the value is 0 for both.

    if fn is not None:
        readstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)
        stonkcpy: Stonk = readstonk.__copy__()

        stonkcpy.toRelative()

        plotStonk(stonkcpy, PlotlyInterface(ticker, title, xaxTitle, yaxTitle), 'h')


def plotStonk(stonk: Stonk, pli: PlotlyInterface, orientation: str):

    poi = []
    coi = []
    pvol = []
    cvol = []

    dt = stonk.expDates[0]

    for o in stonk.options:
        o: Option = o
        if o.expDate == dt:
            oi, vol = (poi, pvol) if o.cop == 'p' else (coi, cvol)
            oi.append(o.oi)
            vol.append(o.vol)

    if orientation == 'v':
        pli.orientation = orientation
        pli.addBar([0] * len(poi), poi, pli.blue, 'put oi', 0)
        pli.addBar([0] * len(coi), coi, pli.red, 'call oi', 0)
        pli.addLine([0] * len(pvol), pvol, pli.blue, 'put vol', 0)
        pli.addLine([0] * len(cvol), cvol, pli.red, 'call vol', 0)

    pli.showGraph(stonk.currentPrice)


# def plotRelativeModel(rel: RelativeCoordinates, pli: PlotlyInterface, ori, offset):
#     cvx = list(rel.callVol.values())
#     cvy = list(rel.callVol.keys())
#     pvx = list(rel.putVol.values())
#     pvy = list(rel.putVol.keys())
#     cox = list(rel.callOI.values())
#     coy = list(rel.callOI.keys())
#     pox = list(rel.putOI.values())
#     poy = list(rel.putOI.keys())
#
#     # print(f'len cvx: {len(cox)}, len cvy: {len(coy)}')
#     # print(f'len pox: {len(pox)}, len poy: {len(poy)}')
#
#     if ori == 'v':
#         pli.orientation = ori
#         pli.addBar(coy, cox, pli.red, 'callOI', offset)
#         pli.addBar(poy, pox, pli.blue, 'putOI', offset)
#         pli.addLine(cvy, cvx, pli.red, 'callVol', offset)
#         pli.addLine(pvy, pvx, pli.blue, 'putVol', offset)
#
#     elif ori == 'h':
#         pli.addLine(cvx, cvy, pli.red, 'callVol', offset)
#         pli.addLine(pvx, pvy, pli.blue, 'putVol', offset)
#         pli.addBar(cox, coy, pli.red, 'callOI', offset)
#         pli.addBar(pox, poy, pli.blue, 'putOI', offset)


# def calcMaxPain(curprice, dopt: DaysOptions):
#     mp = {}
#
#     for st in dopt.straddles:
#         st: Straddle = st
#         dif = abs(curprice - st.strike)
#         cval = st.call.oi * st.call.contractPrice
#         pval = st.put.oi * st.put.contractPrice
#         val = dif * (cval + pval)
#         mp.update({st.strike: val})
#
#     vals = list(mp.values())
#     keys = list(mp.keys())
#     ind = vals.index(max(vals))
#
#     return keys[ind]


if __name__ == '__main__':
    main()
