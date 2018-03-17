import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from pandas import read_csv
from pandas import to_datetime
import pandas as pd

#df = read_csv('datasets/cbk_analysis_v1.csv', sep=';', encoding='latin_1')

df = read_csv('../datasets/DemoConciliacaoVendasIR2018.csv', sep=';', encoding='latin_1')
df['data_compra'] = to_datetime(df['data_compra']).map(lambda x: x.date())
#df['data_compra'] = df['data_compra'].map(lambda x: x.date())


df_hist = df
df_hist = df[['data_compra', 'VlrCompra']].groupby(['data_compra']).sum().sort_values(by=['VlrCompra'], ascending=False)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash()

app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

app.layout = html.Div(children=[
    html.H1(
        children='Conciliação de Vendas',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(children='Última atualização: ' + datetime.strftime(datetime.now(), "%d/%m/%Y")),
    dcc.Graph(
        id='graph1',
        figure={
            'data': [
                {'x': df_hist.index, 'y': df_hist['VlrCompra'],
                 'type': 'bar',
                 'name': 'Vendas'
                },
                {'x': df_hist.index, 'y': df_hist['VlrCompra'], 'type': 'bar',
                 'name': 'Vendas'}
            ],
            'layout': {
                'title': 'Evolução do Chargeback',
                'barmode': 'stack'
            }
        }
    ),
    generate_table(df)
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})



# Run application
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
