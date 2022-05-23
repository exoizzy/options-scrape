import plotly.graph_objects as go

class PlotlyInterface:
    barmode = ['relative', 'stack', 'group', 'overlay']
    baropacity = 0.75
    orientation = 'h'
    linewidth = 2
    showgrid=dict(showgrid=True)
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

    def showGraph(self):
        self.fig.update_layout(
            title=self.title,
            xaxis_title=self.xaxTitle,
            yaxis_title=self.yaxTitle,
            barmode=self.barmode[0],
            xaxis=self.showgrid,
            yaxis=self.showgrid
        )

        self.fig.show()