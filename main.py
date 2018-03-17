import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from pandas import read_csv

#df = read_csv('datasets/cbk_analysis_v1.csv', sep=';', encoding='latin_1').head(20)

df = read_csv('datasets/DemoConciliacaoVendasIR2018.csv', sep=';', encoding='latin_1').head(20)


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
        children='Monitor de Conciliação das Vendas',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(children='Última atualização: ' + datetime.strftime(datetime.now(), "%d/%m/%Y")),
    dcc.Graph(
        id='graph1',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': [100, 200, 300, 200, 300, 400, 500, 500, 400], 'type': 'bar',
                 'name': 'Vendas'},
                {'x': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': [100, 200, 300, 200, 300, 400, 400, 300, 100], 'type': 'line',
                 'name': 'Chargeback'}
            ],
            'layout': {
                'title': 'Evolução do Chargeback'
            }
        }
    ),
    generate_table(df)
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})



# Run application
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
