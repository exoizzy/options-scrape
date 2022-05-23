import plotly.graph_objects as go
from models.RelativeModels import RelativeCoordinates

class PlotlyInterface:
    barmode = ['relative', 'stack', 'group', 'overlay']
    ticklabelpos = ['outside', 'inside', 'outside top', 'inside top', 'outside left', 'inside left', 'outside right',
                    'inside right', 'outside bottom', 'inside bottom']
    baropacity = 0.5
    orientation = 'h'
    legend = dict(
        orientation=orientation,
        yanchor='bottom',
        y=1,
        xanchor='left',
        x=0
    )
    sideright = dict(side='right')
    linewidth = 2
    showgrid = dict(showgrid=True)
    red = 'firebrick'
    blue = 'royalblue'
    fig = None

    def __init__(self, ticker, title, xtitle, ytitle):
        self.ticker, self.title, self.xaxTitle, self.yaxTitle = ticker, title, xtitle, ytitle
        self.fig = go.Figure()

    def addLine(self, xarr, yarr, color, name):
        self.fig.add_trace(
            go.Scatter(
                x=xarr,
                y=yarr,
                name=name,
                line=dict(color=color, width=self.linewidth)
            )
        )

    def addNextLine(self, xar, yar, color, name):
        self.fig.add_trace(
            go.Scatter(
                x=xar,
                y=yar,
                name=name,
                line=dict(color=color, width=self.linewidth),
                base=1
            )
        )

    def addBar(self, xarr, yarr, color, name):
        self.fig.add_trace(
            go.Bar(
                name=name,
                x=xarr,
                y=yarr,
                orientation=self.orientation,
                marker=dict(color=color),
                opacity=self.baropacity
            )
        )

    def addNextBar(self, xarr, yarr, color, name):
        self.fig.add_trace(
            go.Bar(
                name=name,
                x=xarr,
                y=yarr,
                orientation=self.orientation,
                marker=dict(color=color),
                opacity=self.baropacity,
                base=1
            )
        )

    def showGraph(self, curprice):
        if self.orientation == 'v':
            self.fig.add_vline(x=curprice)
        elif self.orientation == 'h':
            self.fig.add_hline(y=curprice)
        ax = {}
        ax.update(self.showgrid)
        ax.update(self.sideright)
        self.fig.update_layout(
            title=self.title,
            legend=self.legend,
            xaxis_title=self.xaxTitle,
            yaxis_title=self.yaxTitle,
            barmode=self.barmode[3],
            xaxis=self.showgrid,
            yaxis=ax
        )

        self.fig.show()