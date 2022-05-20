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
    fn = 'SPY_2022-05-20_test-05202022_stonk.json'
    # yfi = YahooFinanceInterface(ticker)
    # stonk = yfi.get_stonk()
    #
    # if stonk is not None:
    #     fn = FileUtility.saveStonkToJsonFile(stonk, 'test-05202022')
    #
    #     ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)
    #
    #     rel = StonkToRelative.daysOptionsToRelative(ftstonk.options[0], ftstonk.lastOpen)
    #
    #     fig = go.Figure()
    #     fig.add_trace(
    #         go.Scatter(x=list(rel.callVol.values()), y=list(rel.callVol.keys()),
    #                    mode='lines',
    #                    name='callVol')
    #     )
    #     fig.add_trace(
    #         go.Scatter(x=list(rel.putVol.values()), y=list(rel.putVol.keys()),
    #                    mode='lines',
    #                    name='putVol')
    #     )
    #
    #     fig.show()
    # else:
    #     print('stonk is none :( \n')
    barmode=['relative', 'stack', 'group', 'overlay']
    baropacity = 0.75
    orientation = 'v' # 'h'
    linewidth = 3
    red = 'firebrick'
    blue = 'royalblue'

    ftstonk: Stonk = FileUtility.importStonkFromJsonFile(ticker, fn)

    rel = StonkToRelative.daysOptionsToRelative(ftstonk.options[0], ftstonk.lastOpen)

    fig = go.Figure()

    # lines
    fig.add_trace(
        go.Scatter(y=list(rel.callVol.values()), x=list(rel.callVol.keys()),
                   mode='lines',
                   name='callVol',
                   line=dict(color=red, width=linewidth)
        )
    )

    fig.add_trace(
        go.Scatter(y=list(rel.putVol.values()), x=list(rel.putVol.keys()),
                   mode='lines',
                   name='putVol',
                   line=dict(color=blue, width=linewidth)
        )
    )

    # bars
    fig.add_trace(
        go.Bar(
            name='callOI',
            y=list(rel.callOI.values()),
            x=list(rel.callOI.keys()),
            orientation=orientation,
            marker=dict(color=red),
            opacity=baropacity
        )
    )
    fig.add_trace(
        go.Bar(
            name='putOI',
            y=list(rel.putOI.values()),
            x=list(rel.putOI.keys()),
            orientation=orientation,
            marker=dict(color=blue),
            opacity=baropacity
        )
    )

    fig.update_layout(title='relative with old oi calcs', xaxis_title='vol && oi (value/max as % of time to expiry)',
                      yaxis_title='strike price ($)', barmode=barmode[0] #, xaxis=dict(categoryorder='total descending')
    )

    fig.show()


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
