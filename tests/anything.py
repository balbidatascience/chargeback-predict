from pandas import read_csv
from pandas import to_datetime
import pandas as pd

df = read_csv('../datasets/DemoConciliacaoVendasIR2018.csv', sep=';', encoding='latin_1')
df['data_compra'] = to_datetime(df['data_compra']).map(lambda x: x.date())
df_hist = df
df_hist = df[['data_compra', 'Conciliado', 'VlrCompra']].groupby(['data_compra', 'Conciliado']).sum()
df_hist.reset_index(level=['data_compra', 'Conciliado'], inplace=True)

df_hist['mes'] = to_datetime(df_hist['data_compra']).map(lambda x: x.date().day)

print(df['data_compra'])

print(df_hist.dtypes)

print(df_hist['mes'].unique())