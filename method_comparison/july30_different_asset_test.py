import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import yfinance as yf

df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')
df_GLD = yf.download ('GLD', '2018-01-01', '2023-12-31')
df_SPY.columns = df_SPY.columns.get_level_values(0)
df_GLD.columns = df_GLD.columns.get_level_values(0)

close_SPY = df_SPY["Close"]
close_GLD = df_GLD["Close"]
SPY_returns = np.log(close_SPY/close_SPY.shift(1)).dropna()
SPY_vol = SPY_returns.rolling(window=20).std().dropna()
GLD_returns = np.log(close_GLD/close_GLD.shift(1)).dropna()
GLD_vol = GLD_returns.rolling(window=20).std().dropna()
corr = SPY_returns.rolling(window=20).corr(GLD_returns)

df_SPY['returns'] = SPY_returns
df_SPY['vol']= SPY_vol
df_SPY['corr'] = corr
df_GLD['returns'] = GLD_returns
df_GLD['vol'] = GLD_vol

SPY_df_clean = df_SPY.dropna().copy()
GLD_df_clean = df_GLD.dropna().copy()
x = SPY_df_clean[['returns', 'vol', 'corr']]
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x)
SPY_df_clean['cluster'] = labels

print("labels; ", labels)
print("lenght: ", len(labels))
print("shape: ", labels.shape)
print("Cluster value counts:", SPY_df_clean['cluster'].value_counts())
print("Cluster averages (returns, vol):", SPY_df_clean.groupby('cluster')[['returns', 'vol']].mean())