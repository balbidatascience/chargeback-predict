import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from datetime import datetime
from pandas import read_csv
from pandas import to_datetime
import pandas as pd

df = read_csv('../datasets/DemoConciliacaoVendasIR2018.csv', sep=';', encoding='latin_1')
df['data_compra'] = to_datetime(df['data_compra']).map(lambda x: x.date())
df_hist = df
df_hist = df[['data_compra', 'Conciliado', 'VlrCompra']].groupby(['data_compra', 'Conciliado']).sum()
df_hist.reset_index(level=['data_compra', 'Conciliado'], inplace=True)


def generate_bar(df):
    pv = pd.pivot_table(df, index=['data_compra'], columns=["Conciliado"], values=['VlrCompra'], aggfunc=sum,
                        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[('VlrCompra', 'Conciliada')], name='Conciliada', marker={'color': '#16AFA6'})
    trace2 = go.Bar(x=pv.index, y=pv[('VlrCompra', 'Divergente')], name='Divergente', marker={'color': '#C34C83'})
    trace3 = go.Bar(x=pv.index, y=pv[('VlrCompra', 'Em aberto')], name='Em aberto', marker={'color': '#5F3352'})

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3],
            'layout':
                go.Layout(
                    title='Status das Vendas',
                    barmode='stack',
                    xaxis={
                        'rangeselector': {
                            'buttons': [
                                {
                                    'step': 'all',
                                    'label': '#reset'
                                },
                                {
                                    'step': 'month',
                                    'label': '#mês',
                                    'stepmode': 'backward',
                                    'count': '1'
                                },
                                {
                                    'step': 'day',
                                    'stepmode': 'backward',
                                    'count': '7',
                                    'label':  '#semana'
                                }
                            ],
                            'font': {'family': '\"Open Sans\", verdana, arial, sans-serif',
                                     "size": '12',
                                     'color': '#444'
                                     }
                        }
                    })
        })


# Start app
app = dash.Dash()

# cach css and scripts
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def generate_slider(df):
    return dcc.Slider(
        id='date-slider',
        min=df.index.min(),
        max=df.index.max(),
        value='0',
        marks={str(data): str(data) for data in [0, df.index.max() / 2, df.index.max()]}
    )


app.layout = html.Div(children=[
    html.H1(
        children='Conciliação de Vendas',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(children='Última atualização: ' + datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")),
    generate_bar(df),
    dcc.Graph(
        id='graph1',
        figure={
            'data': [
                {'x': df_hist.index, 'y': df_hist['VlrCompra'],
                 'type': 'bar',
                 'name': 'Vendas'
                 },
                {'x': df_hist.index, 'y': df_hist['VlrCompra'], 'type': 'bar',
                 'name': 'CBK'}
            ],
            'layout': {
                'title': 'Evolução do Chargeback',
                'barmode': 'relative'
            }
        }
    ),
    generate_slider(df_hist),
    generate_table(df)  # ,
    # dcc.Graph(id='graph-with-slider'),

])

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# Run application
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
