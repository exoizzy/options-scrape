import plotly.graph_objects as go
from models.RelativeModels import RelativeCoordinates


class PlotlyInterface:
    barmode = ['relative', 'stack', 'group', 'overlay']
    ticklabelpos = ['outside', 'inside', 'outside top', 'inside top', 'outside left', 'inside left', 'outside right',
                    'inside right', 'outside bottom', 'inside bottom']
    baropacity = 0.75
    lineopacity = 0.5
    orientation = 'h'
    legend = dict(
        orientation=orientation,
        yanchor='bottom',
        y=1,
        xanchor='left',
        x=0
    )
    sideright = dict(side='right')
    linewidth = 1
    showgrid = dict(showgrid=True)
    red = 'firebrick'
    blue = 'royalblue'
    fig = None

    def __init__(self, ticker, title, xtitle, ytitle):
        self.ticker, self.title, self.xaxTitle, self.yaxTitle = ticker, title, xtitle, ytitle
        self.fig = go.Figure()

    """
    add line to self.fig
    """
    def addLine(self, xarr, yarr, color, name, offset):
        # so i think here i can basically just add 1 to every x/y (depending on which is the actual vol value
        # and that will offset the graph to where i want it and we can just figure out the actual like Te offsets later
        if self.orientation == 'v':
            self.offsetValues(yarr, offset)
        elif self.orientation == 'h':
            self.offsetValues(xarr, offset)

        self.fig.add_trace(
            go.Scatter(
                x=xarr,
                y=yarr,
                name=name,
                line=dict(color=color, width=self.linewidth),
                opacity=self.lineopacity
            )
        )

    """
    add bar to self.fig
    """
    def addBar(self, xarr, yarr, color, name, offset):
        if offset == 0:
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
        else:
            self.fig.add_trace(
                go.Bar(
                    name=name,
                    x=xarr,
                    y=yarr,
                    orientation=self.orientation,
                    marker=dict(color=color),
                    opacity=self.baropacity,
                    base=offset
                )
            )

    """
    increments array values based on the given offset
    doing this to allow plotting of multiple days on a single graph, and since all values are <= 1 we can simply
    add 1*num_prev_exp_dates to the values of a given expiry's values and offset the graph the correct amount
    """
    def offsetValues(self, arr: list, offset):
        for i in range(0, len(arr)):
            arr[i] = arr[i] + offset

    """
    opens the graph with plotly.graph_object.Figure.show() would, adds some formatting things to properly display
    the graph(s) as i would like
    """
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
            yaxis=ax,
            showlegend=False
        )

        self.fig.show()
