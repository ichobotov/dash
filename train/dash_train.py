import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc


# Считываем данные
# df = pd.read_csv('data.csv')
# df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="%d.%m.%Y")

# df.index = pd.to_datetime(df['Date'])



def get_graphs(df, players = []):

    graphs_list = []
    # if players is None:
    #     for param in df[["MSM availability","PPP availability","Mean Nsat tracked","Mean Nsat used in PPP","PPP H95","P2P PPP H95","P2P Struna H95"]]:
    #          graphs_list.append(dcc.Graph(id='graphs',
    #                    # config={'displayModeBar': False},
    #                    # animate=True,
    #                    figure=px.line(df, x='Date', y=param, title=param)))
            # html_list.append(dcc.Graph)
    # else:
    if len(players) == 1:
        for param in df[
            ["MSM availability", "PPP availability", "Mean Nsat tracked", "Mean Nsat used in PPP", "PPP H95","P2P PPP H95", "P2P Struna H95"]]:
            graphs_list.append(dcc.Graph(id='graphs',
                                         # config={'displayModeBar': False},
                                         # animate=True,
                                         figure=px.line(df, x='Date', y=param, title=param, color='Location')))
        return graphs_list
    print(f'dff to graph \n {df}')
    for param in df[["MSM availability","PPP availability","Mean Nsat tracked","Mean Nsat used in PPP","PPP H95","P2P PPP H95","P2P Struna H95"]]:
         if not param in ["PPP availability","Mean Nsat used in PPP","PPP H95","P2P PPP H95","P2P Struna H95"]:
             any_player = int(df['PVT'].unique()[0])
             graphs_list.append(dcc.Graph(id='graphs',
                       # config={'displayModeBar': False},
                       # animate=True,

                       figure=px.line(df[df['PVT'] == any_player], x='Date', y=param, title=param, color='Location')))
         else:
            mich = [player for player in players if 'mich' in player]
            barn = [player for player in players if 'barn' in player]
            if len(mich) != 0 and len(barn) != 0:
                used_players = list(df['PVT'].unique())
                for player in used_players:
                    graphs_list.append(dcc.Graph(id='graphs',
                                                 # config={'displayModeBar': False},
                                                 # animate=True,
                                                 figure=px.line(df[df['PVT']==player], x='Date', y=param, title=f'{param} for PVT player {player}', color='Location')))
            else:
                graphs_list.append(dcc.Graph(id='graphs',
                                             # config={'displayModeBar': False},
                                             # animate=True,
                                             figure=px.line(df, x='Date', y=param, title=param, color='PVT')))

    return graphs_list


#отрисовка нескольких плееров
mich_players = ['mich_PVT_01.csv', 'mich_PVT_02.csv', 'mich_PVT_03.csv']
barn_players = ['barn_PVT_01.csv', 'barn_PVT_02.csv', 'barn_PVT_03.csv']
df_list = []
for data in mich_players:
    df = pd.read_csv('mich_PVT_01.csv')
    df_list.append(df)

for data in barn_players:
    df = pd.read_csv('barn_PVT_01.csv')
    df_list.append(df)

df = pd.concat(df_list)
# fig = px.line(df,
#               x='Date', y='P2P Struna H95', color='PVT', title='P2P Struna H95')
# fig.show()



# Инициализируем сервер
app = Dash(__name__)

# Разграничиваем плоскость дашборда
app.layout = html.Div(
    children=[
        html.H1('PPP statistics'),
        html.P('''Выберите даты'''),
         html.Div(
             dcc.DatePickerRange(
                 id="date-range",
                 min_date_allowed=min(df["Date"]),
                 max_date_allowed=max(df["Date"]),
                 end_date=max(df["Date"]),
                 start_date=min(df["Date"]),
                 # clearable=True,
                reopen_calendar_on_clear=True,
                updatemode='bothdates',
                 persistence=True
             )
        ),
        html.Button('Reset Date', id='reset-date', n_clicks=0),
        html.P('Choose PVT player'),
        dcc.Dropdown(
            id="players-select",
            value=[],
            options=[],
            multi=True,
            style = {
                    # 'display': 'block',
                    'width': '39%',
                    # 'height': 100,
                    'margin-top': '2%',
                    # 'margin-left': '14%',
                    # 'background-color': '#F6FBFF',
                    # 'border-color': '#DFE6E9',
                    # 'textAlign': 'center',
                    # 'font-family': 'Arial',
                    # 'font-size': '40px',
                    # 'verticalAlign': 'middle',
                    # 'justify-content': 'center',
                },
        ),
            html.P("Choose Data set"),
            dcc.Checklist(
                        id="data_set",
                        options=["Mich", "Barn"],
                        value=["Mich", "Barn"],
                        inline=True,
                    ),
        html.Div(id='graph_list',
                 children=get_graphs(df)

                 ),
         dcc.Interval('graph-update', interval = 86400000, n_intervals = 0)
    ]
)

@app.callback(
        # [Output('graph_list','children'),
        [Output('date-range','start_date'),
         Output('date-range','end_date'),
         Output('date-range','min_date_allowed'),
         Output('date-range','max_date_allowed')],
        [Input('graph-update', 'n_intervals'),
        Input('reset-date', 'n_clicks')]
         )
def update(n,n_clicks):
    df = pd.read_csv('mich_PVT_01.csv')
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    # dff = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    return min(df["Date"]), max(df["Date"]), min(df["Date"]), max(df["Date"])


@app.callback(
    Output("graph_list", "children"),
    [Input("date-range", "start_date"),
    Input("date-range", "end_date"),
     Input("players-select", "value"),
     Input("data_set", "value")]
)
def render_content(start_date, end_date, players, location):
    print(f'players from render{players}')
    # print(type(players))
    # dff = df.query("Date > @start_date & Date < @end_date")
    df_list = []
    for data in players:
        df = pd.read_csv(data)
        df_list.append(df)
    df = pd.concat(df_list)
    # df = pd.read_csv('data.csv')
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    dff = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    print(dff)
        # [(df['B'] < 8) & (df['B'] > 2)]
    return get_graphs(dff, players)

@app.callback(
    [Output("players-select", "value"),
     Output("players-select", "options")],
    Input("data_set", "value"))
def update_data_set(location):
    players = []
    for data in location:
        if 'Mich' in data:
            players.append(mich_players[0])
        elif 'Barn' in data:
            players.append(barn_players[0])
        print(data)
    print(f'players {players}')
    return players



            #              dcc.Graph(id='timeseries',
                    #                 config={'displayModeBar': False},
                    #                 animate=True,
                    #                 figure=[px.line(df,x='Date',y='PPP availability'),
                    #                        px.line(df,
                    #                                       x='Date',
                    #                                       y='PPP availability')]
                    #              #           )
                    #
                    #                                             ),
                    #              # dcc.Graph(id='timeseries2',
                    #              #           config={'displayModeBar': False},
                    #              #           animate=True,
                    #              #           figure=px.line(df,
                    #              #                          x='Date',
                    #              #                          y='PPP availability')
                    #              #           )
                    #
                    #          ])
                    # ])
        # ]

# )



#ШАГ 2---------------------------------------------------------------

#ШАГ 3---------------------------------------------------------------
# Выводим временные ряды с ценниками акций
# app.layout = html.Div(
#     children=[
#         html.Div(className='row',
#                  children=[
#                     html.Div(className='four columns div-user-controls',
#                              children=[
#                                             html.H2('Dash - пример'),
#                                             html.P('''Визуализация рядов'''),
#                                             html.P('''Выберете одну или несколько акций''')
#                                 ]
#                              ),
#                     html.Div(className='eight columns div-for-charts bg-grey',
#                              children=[
#                                  dcc.Graph(id='timeseries',
#                                     config={'displayModeBar': False},
#                                     animate=True,
#                                     figure=px.line(df,
#                                                     x='Date',
#                                                     y='value',
#                                                     color='stock',
#                                                     template='plotly_dark').update_layout(
#                                                             {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#                                                                 )
#                                         ])
#                               ])
#         ]

# )
#ШАГ 3---------------------------------------------------------------
#
#
# def get_options(list_stocks):
#     dict_list = []
#     for i in list_stocks:
#         dict_list.append({'label': i, 'value': i})
#
#     return dict_list

#ШАГ 4---------------------------------------------------------------
# Добавим меню для выбора акций для отображения их временных рядов на графике
# app.layout = html.Div(
#     children=[
#         html.Div(className='row',
#                  children=[
#                     html.Div(className='four columns div-user-controls',
#                              children=[
#                                             html.H2('Dash - пример'),
#                                             html.P('''Визуализация рядов'''),
#                                             html.P('''Выберете одну или несколько акций'''),
#                                             html.Div(className='div-for-dropdown',
#                                                         children=[
#                                                             dcc.Dropdown(id='stockselector',
#                                                                         options=get_options(df['stock'].unique()),
#                                                                         multi=True,
#                                                                         value=[df['stock'].sort_values()[0]],
#                                                                         style={'backgroundColor': '#1E1E1E'},
#                                                                         className='stockselector')
#                                                                     ],
#                                                         style={'color': '#1E1E1E'})
#                                 ]
#                              ),
#                     html.Div(className='eight columns div-for-charts bg-grey',
#                              children=[
#                                  dcc.Graph(id='timeseries',
#                                     config={'displayModeBar': False},
#                                     animate=True,
#                                     figure=px.line(df,
#                                                     x='Date',
#                                                     y='value',
#                                                     color='stock',
#                                                     template='plotly_dark').update_layout(
#                                                             {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#                                                                 )
#                                         ])
#                               ])
#         ]
# )
#ШАГ 4---------------------------------------------------------------


#ШАГ 5---------------------------------------------------------------
# Свяжем меню выбора названия акции с отображением ее временного ряда на графике
# app.layout = html.Div(
#     children=[
#         html.Div(className='row',
#                  children=[
#                     html.Div(className='four columns div-user-controls',
#                              children=[
#                                 html.H2('Dash - пример'),
#                                 html.P('''Визуализация рядов'''),
#                                 html.P('''Выберете одну или несколько акций'''),
#                                  html.Div(
#                                      className='div-for-dropdown',
#                                      children=[
#                                          dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
#                                                       multi=True, value=[df['stock'].sort_values()[0]],
#                                                       style={'backgroundColor': '#1E1E1E'},
#                                                       className='stockselector'
#                                                       ),
#                                      ],
#                                      style={'color': '#1E1E1E'})
#                                 ]
#                              ),
#                     html.Div(className='eight columns div-for-charts bg-grey',
#                              children=[
#                                  dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
#                              ])
#                               ])
#         ]

# )

# # Callback
# @app.callback(Output('timeseries', 'figure'),
#               [Input('stockselector', 'value')])
# def update_graph(selected_dropdown_value):
#     trace1 = []
#     df_sub = df
#     for stock in selected_dropdown_value:
#         trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
#                                  y=df_sub[df_sub['stock'] == stock]['value'],
#                                  mode='lines',
#                                  opacity=0.7,
#                                  name=stock,
#                                  textposition='bottom center'))
#     traces = [trace1]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data,
#               'layout': go.Layout(
#                   colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
#                   template='plotly_dark',
#                   paper_bgcolor='rgba(0, 0, 0, 0)',
#                   plot_bgcolor='rgba(0, 0, 0, 0)',
#                   margin={'b': 15},
#                   hovermode='x',
#                   autosize=True,
#                   title={'text': 'Цены акций', 'font': {'color': 'white'}, 'x': 0.5},
#                   xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
#               ),
#
#               }
#
#     return figure
#ШАГ 5---------------------------------------------------------------

# Запускаем приложение
if __name__ == '__main__':
    # app.run_server(debug=True, )
    app.run(host='0.0.0.0', port='8050',debug=True)