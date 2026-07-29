import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import yfinance as yf

df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')
df_QQQ = yf.download ('QQQ', '2018-01-01', '2023-12-31')
df_SPY.columns = df_SPY.columns.get_level_values(0)
df_QQQ.columns = df_QQQ.columns.get_level_values(0)

close_SPY = df_SPY["Close"]
close_QQQ = df_QQQ["Close"]
SPY_returns = np.log(close_SPY/close_SPY.shift(1)).dropna()

window_sizes = [10, 20, 60]

for window in window_sizes:
    SPY_vol = SPY_returns.rolling(window=window).std().dropna()
    QQQ_returns = np.log(close_QQQ/close_QQQ.shift(1)).dropna()
    QQQ_vol = QQQ_returns.rolling(window=window).std().dropna()
    corr = SPY_returns.rolling(window=window).corr(QQQ_returns)

    df_SPY['returns'] = SPY_returns
    df_SPY['vol']= SPY_vol
    df_SPY['corr'] = corr
    df_QQQ['returns'] = QQQ_returns
    df_QQQ['vol'] = QQQ_vol

    SPY_df_clean = df_SPY.dropna().copy()
    QQQ_df_clean = df_QQQ.dropna().copy()
    x = SPY_df_clean[['returns', 'vol', 'corr']]
    model = KMeans(n_clusters=3, random_state=3)
    labels = model.fit_predict(x)
    SPY_df_clean['cluster'] = labels

    print(f"Window size: {window}")
    print("lenght: ", len(labels))
    print("shape: ", labels.shape)
    print("Cluster value counts:", SPY_df_clean['cluster'].value_counts())
    print("Cluster averages (returns, vol):", SPY_df_clean.groupby('cluster')[['returns', 'vol']].mean())
