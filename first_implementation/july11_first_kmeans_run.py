import numpy as np
import pandas as pd
from sklearn.cluster import KMeans 
import yfinance as yf

df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')
df_SPY.columns = df_SPY.columns.get_level_values(0)

close = df_SPY["Close"]
returns = np.log(close/close.shift(1)).dropna()
vol_20 = returns.rolling(window=20).std()

df_SPY['returns']=returns
df_SPY['vol_20']=vol_20

df_clean = df_SPY.dropna().copy()
x = df_clean[['returns', 'vol_20']]
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x)
df_clean['cluster'] = labels

print(labels)
print(len(labels))
print(labels.shape)
print(df_clean['cluster'].value_counts())
print(df_clean.groupby('cluster')[['returns', 'vol_20']].mean())
