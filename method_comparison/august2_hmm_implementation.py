import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import yfinance as yf
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

df = yf.download("NG=F", start="2018-01-01", end="2023-12-31")
df.columns = df.columns.get_level_values(0)
close = df["Close"]

returns = np.log(close / close.shift(1)).dropna()
vol = returns.rolling(window=20).std().dropna()
df["returns"] = returns
df["vol"] = vol
df_clean = df.dropna().copy()
x = df_clean[["returns", "vol"]]

model_KMeans = KMeans(n_clusters=3, random_state=3)
model_KMeans.fit(x)
kmeans_labels = model_KMeans.predict(x)
df_clean["kmeans_labels"] = kmeans_labels
model_HMM = GaussianHMM(n_components=3, covariance_type="full", random_state=3)
model_HMM.fit(x)
hidden_states = model_HMM.predict(x)
df_clean["hidden_states"] = hidden_states
hmm_switches = (df_clean['hidden_states'] != df_clean['hidden_states'].shift(1)).sum()
KMeans_switches = (df_clean['kmeans_labels'] != df_clean['kmeans_labels'].shift(1)).sum()
period_2023 = df_clean.loc['2023-05-30':'2023-10-06']

print("hidden states sizes: ", df_clean["hidden_states"].value_counts())
print("hidden states means: ", df_clean.groupby("hidden_states")[["returns", "vol"]].mean())
print(f"HMM state switches: {hmm_switches}")
print(f"KMeans state switches: {KMeans_switches}")
print(period_2023['hidden_states'].value_counts())