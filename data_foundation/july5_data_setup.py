import numpy as np
import pandas as pd
from sklearn.cluster import KMeans 
import yfinance as yf

df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')

close = df_SPY["Close"]
returns = np.log(close/close.shift(1)).dropna()
vol_20 = returns.rolling(window=20).std()

df_SPY['returns']=returns
df_SPY['vol_20']=vol_20
