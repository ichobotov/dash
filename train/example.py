import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('data.csv')
df2 = pd.read_csv('data_short.csv')

"""
три линейных графика
fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.06,
                    subplot_titles=['Availability','Mean Sat','H95'],
                    x_title='Date',
                   )

fig.add_trace(go.Scatter(x=df['Date'], y=df['MSM availability'],name='MSM availability',legendgroup=0),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['PPP availability'],name='PPP availability',legendgroup=0),
              row=1, col=1 )

fig.add_trace(go.Scatter(x=df['Date'], y=df['Mean Nsat used in PPP'],name='Mean Nsat used in PPP',legendgroup=1),
              row=2, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['Mean Nsat tracked'],name='Mean Nsat tracked',legendgroup=1),
              row=2, col=1)

fig.add_trace(go.Scatter(x=df['Date'], y=df['PPP H95'], name = 'PPP H95',legendgroup=2),
              row=3, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['P2P PPP H95'], name = 'P2P PPP H95',legendgroup=2),
              row=3, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['P2P Struna H95'], name = 'P2P Struna H95',legendgroup=2),
              row=3, col=1)

# fig.update_layout(height=600, width=600,
#                   title_text="Stacked Subplots with Shared X-Axes")

fig.update_layout(title_text="Barnaul", yaxis_title=dict(text='%'), yaxis2_title=dict(text='Sats'), yaxis3_title=dict(text='Meters'),legend_tracegroupgap=60)
# print (fig)
# fig.show()
"""

"""
все бары в одном

df = pd.read_csv('data.csv')

fig1 = go.Figure(data=[
    go.Bar(name='MSM', x=df['Date'], y=df['MSM availability'],opacity=0.5),
    go.Bar(name='PPP', x=df['Date'], y=df['PPP availability'],opacity=0.6)
])
fig2 = go.Figure(data=[
    go.Bar(name='Tracked', x=df['Date'], y=df['Mean Nsat tracked'],opacity=0.5),
    go.Bar(name='Used', x=df['Date'], y=df['Mean Nsat used in PPP'],opacity=0.6)
])
# Change the bar mode
fig1.update_layout(barmode='overlay')
fig2.update_layout(barmode='overlay')

fig = go.Figure(data = fig1.data + fig2.data, layout=fig1.layout)
fig.show()


"""



"""
Bars + Dots by color

fig = go.Figure()

fig.add_trace(go.Bar(x=df['Date'], y=df['MSM availability'],opacity=0.8,marker=dict(color='grey')))
fig.add_trace(go.Bar(x=df['Date'], y=df['PPP availability'],yaxis="y2",opacity=0.5,marker=dict(color='blue')))
fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat tracked'],opacity=0.8))
fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat used in PPP'],yaxis="y2",opacity=0.8))
fig.update_layout(barmode='group')
fig.update_layout(
    xaxis=dict(
        visible=True
    ),
    # yaxis=dict(
    #     title="yaxis title",
    # ),
    yaxis=dict(
            title="yaxis2 title",
            # overlaying="y",
            # side="left",
            range=[0,100],
            # visible=True
        ),
    yaxis2=dict(
        title="yaxis2 title",
        overlaying="y",
        side="right",
        range=[0,100],
        visible=False
    ),
)



fig2 = go.Figure()

def SetColor(df,column,column2,threshold):
    values = df[column].tolist()
    print(len(values))
    color_list = []
    for i in values:
        if(float(df.loc[df['Date']==i, column2]) < threshold):
            color_list.append("green")
            # return 'blue'
        elif(float(df.loc[df['Date']==i, column2]) >= threshold):
            color_list.append("red")
            # return 'red'
        # elif(float(df.loc[df['Date']==i, column2])>=0.08):
        #     color_list.append("green")
            # return 'green'
    print(len(color_list))
    return color_list


fig2.add_trace(go.Scatter(
        x=df['Date'].tolist(),
        y=[1 for _ in range(len(df['Date']))],
        mode="markers",

        # mode='markers',
        marker=dict(
            size=20,
            symbol='square',
            color= SetColor(df, 'Date', 'PPP H95', 0.08)  #function gets called here and will return a list of colors, (i.e. ['green', 'blue', 'red', 'green'])
        ),
    )
)

fig2.add_trace(go.Scatter(
        x=df['Date'].tolist(),
        y=[2 for _ in range(len(df['Date']))],
        mode="markers",

        # mode='markers',
        marker=dict(
            size=20,
            symbol='square',
            color= SetColor(df, 'Date', 'P2P PPP H95', 0.18)  #function gets called here and will return a list of colors, (i.e. ['green', 'blue', 'red', 'green'])
        ),
    )
)

fig2.add_trace(go.Scatter(
        x=df['Date'].tolist(),
        y=[3 for _ in range(len(df['Date']))],
        mode="markers",

        # mode='markers',
        marker=dict(
            size=20,
            symbol='square',
            color= SetColor(df, 'Date', 'P2P Struna H95', 0.27)  #function gets called here and will return a list of colors, (i.e. ['green', 'blue', 'red', 'green'])
        ),
    )
)
fig2.update_layout(
    xaxis=dict(
        title="yaxis title",
        range=[-0.5, len(df['Date'])-0.5],
    )
)

"""


# fig1 = go.Figure(data=[
#     go.Bar(name='MSM', x=df['Date'], y=df['MSM availability'],opacity=0.5, barmode='overlay'),
#     go.Bar(name='PPP', x=df['Date'], y=df['PPP availability'],opacity=0.6)
# ])
# fig2 = go.Figure(data=[
#     go.Bar(name='Tracked', x=df['Date'], y=df['Mean Nsat tracked'],opacity=0.5),
#     go.Bar(name='Used', x=df['Date'], y=df['Mean Nsat used in PPP'],opacity=0.6)
# ])
# # Change the bar mode
# fig1.update_layout(barmode='group')
# fig2.update_layout(barmode='overlay')
#
# fig = go.Figure(data = fig1.data + fig2.data, layout=fig1.layout)
# fig = make_subplots(rows=2, cols=1,
#                     shared_xaxes=True,
#                     # vertical_spacing=0.06,
#                     # subplot_titles=['Availability','Mean Sat','H95'],
#                     x_title='Date',
#                    )

# Create a figure with the right layout
#
# fig = make_subplots(rows=2, cols=1,
#                     shared_xaxes=True,
#                     row_heights = [0,100],
#                     # vertical_spacing=0.06,
#                     # subplot_titles=['Availability','Mean Sat','H95'],
#                     # x_title='Date',
#                    )
# fig = go.Figure()

# fig.add_trace(go.Bar(x=df['Date'], y=df['MSM availability']))
# fig.add_trace(go.Bar(x=df['Date'], y=df['PPP availability'],yaxis="y2"))
# fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat tracked']))
# fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat used in PPP'],yaxis="y2"))
# fig.add_trace(go.Line(x=df['Date'], y=df['PPP H95'], yaxis="y3"))
# fig.add_trace(go.Line(x=df['Date'], y=df['P2P PPP H95'], yaxis="y3"))
# fig.add_trace(go.Line(x=df['Date'], y=df['P2P Struna H95'], yaxis="y3"))


fig = go.Figure()

fig.add_trace(go.Bar(x=df['Date'], y=df['MSM availability'],opacity=0.8,marker=dict(color='grey')))
fig.add_trace(go.Bar(x=df['Date'], y=df['PPP availability'],yaxis="y2",opacity=0.5,marker=dict(color='blue')))
fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat tracked'],opacity=0.8))
fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat used in PPP'],yaxis="y2",opacity=0.8))
# fig.update_traces(width=1)
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Date'], y=df['PPP H95'],line=dict(color='yellow',width=2)))
fig2.add_trace(go.Scatter(x=df['Date'], y=df['P2P PPP H95'],line=dict(color='red',width=2)))
fig2.add_trace(go.Scatter(x=df['Date'], y=df['P2P Struna H95'],line=dict(color='saddlebrown',width=2)))

fig2.update_layout(
    xaxis=dict(
        title="yaxis title",
        range=[-0.5, len(df['Date'])-0.5],
    ),
    yaxis=dict(
            title="yaxis title",
            range=[0,0.5],
        )
)

# fig.add_trace(go.Bar(x=df['Date'], y=df['MSM availability']),row=1, col=1, secondary_y=False)
# fig.add_trace(go.Bar(x=df['Date'], y=df['PPP availability']),row=1, col=1, secondary_y=True)
# fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat tracked']),row=1, col=1, secondary_y=False)
# fig.add_trace(go.Bar(x=df['Date'], y=df['Mean Nsat used in PPP']),row=1, col=1, secondary_y=True)
# fig.add_trace(go.Scatter(x=df['Date'], y=df['PPP H95']),row=2, col=1, secondary_y=True)
# fig.add_trace(go.Scatter(x=df['Date'], y=df['P2P PPP H95']),row=2, col=1, secondary_y=True)
# fig.add_trace(go.Scatter(x=df['Date'], y=df['P2P Struna H95']),row=2, col=1, secondary_y=True)
fig.update_layout(barmode='group')
fig.update_layout(
    xaxis=dict(
        visible=True
    ),
    # yaxis=dict(
    #     title="yaxis title",
    # ),
    yaxis=dict(
            title="yaxis2 title",
            # overlaying="y",
            # side="left",
            range=[0,100],
            # visible=True
        ),
    yaxis2=dict(
        title="yaxis2 title",
        overlaying="y",
        side="right",
        range=[0,100],
        visible=False
    ),
)


app = Dash(__name__)

# Разграничиваем плоскость дашборда
app.layout = html.Div(
    children=[
        html.H1('PPP statistics'),
        # html.P('''Выберите даты'''),
        #  html.Div(
        #      dcc.DatePickerRange(
        #          id="date-range",
        #          min_date_allowed=min(df["Date"]),
        #          max_date_allowed=max(df["Date"]),
        #          end_date=max(df["Date"]),
        #          start_date=min(df["Date"]),
        #          # clearable=True,
        #         reopen_calendar_on_clear=True,
        #         updatemode='bothdates',
        #          persistence=True
        #      )
        # ),
        # html.Button('Reset Date', id='reset-date', n_clicks=0),
        # html.P('Choose PVT player'),
        # dcc.Dropdown(
        #     id="players-select",
        #     value=[],
        #     options=[],
        #     multi=True,
        #     style = {
        #             # 'display': 'block',
        #             'width': '39%',
        #             # 'height': 100,
        #             'margin-top': '2%',
        #             # 'margin-left': '14%',
        #             # 'background-color': '#F6FBFF',
        #             # 'border-color': '#DFE6E9',
        #             # 'textAlign': 'center',
        #             # 'font-family': 'Arial',
        #             # 'font-size': '40px',
        #             # 'verticalAlign': 'middle',
        #             # 'justify-content': 'center',
        #         },
        # ),
        #     html.P("Choose Data set"),
        #     dcc.Checklist(
        #                 id="data_set",
        #                 options=["Mich", "Barn"],
        #                 value=["Mich", "Barn"],
        #                 inline=True,
        #             ),
        dcc.Graph(id='graph_list',
                 figure=fig

                 ),
        dcc.Graph(id='graph_list',
                         figure=fig2

                         ),

        # dcc.Interval('graph-update', interval = 86400000, n_intervals = 0)
    ]
)
if __name__ == '__main__':
    # app.run_server(host = '0.0.0.0',debug=True, )
    app.run_server(host = '0.0.0.0',debug  =True, )


