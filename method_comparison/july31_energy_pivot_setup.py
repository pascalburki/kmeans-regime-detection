import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df_NG = yf. download('NG=F', '2018-01-01', '2023-12-31')
df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')
df_NG.columns = df_NG.columns.get_level_values(0)  
df_SPY.columns = df_SPY.columns.get_level_values(0)  


close_NG = df_NG["Close"]
close_SPY = df_SPY["Close"]
returns_NG = np.log(close_NG/close_NG.shift(1)).dropna()
returns_SPY = np.log(close_SPY/close_SPY.shift(1)).dropna()
vol_20_NG = returns_NG.rolling(window=20).std().dropna()
vol_20_SPY = returns_SPY.rolling(window=20).std().dropna()
df_NG["returns"] = returns_NG
df_NG["vol_20"] = vol_20_NG
df_SPY["returns"] = returns_SPY
df_SPY["vol_20"] = vol_20_SPY
df_NG_clean = df_NG.dropna().copy()
x = df_NG_clean[['returns', 'vol_20']]
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x)
df_NG_clean['cluster'] = labels
cluster_0_days = df_NG_clean[df_NG_clean['cluster'] == 0]
cluster_1_days = df_NG_clean[df_NG_clean['cluster'] == 1]
cluster_2_days = df_NG_clean[df_NG_clean['cluster'] == 2]

print("mean returns: ", round(returns_NG.mean(), 4))
print("mean vol: ", round(vol_20_NG.mean(), 4))
cluster_averages = df_NG_clean.groupby('cluster')[['returns', 'vol_20']].mean()

print("cluster size: ", len(cluster_0_days))
print("Cluster 0 averages (returns, vol):", cluster_averages.loc[0])
print("Cluster 0 range: ", cluster_0_days.index.min(), "to", cluster_0_days.index.max())
print("Cluster 0 year distribution:", cluster_0_days.index.month.value_counts().sort_index())
print("Cluster 0 year distribution:", cluster_0_days.index.year.value_counts().sort_index())
print()

print("cluster size: ", len(cluster_1_days))
print("Cluster 1 averages (returns, vol):", cluster_averages.loc[1])
print("Cluster 1 range: ", cluster_1_days.index.min(), "to", cluster_1_days.index.max())
print("Cluster 1 year distribution:", cluster_1_days.index.month.value_counts().sort_index())
print("Cluster 1 year distribution:", cluster_1_days.index.year.value_counts().sort_index())
print()

print("cluster size: ", len(cluster_2_days))
print("Cluster 2 averages (returns, vol):", cluster_averages.loc[2])
print("Cluster 2 range: ", cluster_2_days.index.min(), "to", cluster_2_days.index.max())
print("Cluster 2 year distribution:", cluster_2_days.index.month.value_counts().sort_index())
print("Cluster 2 year distribution:", cluster_2_days.index.year.value_counts().sort_index())
print()

plt.plot(returns_NG, color='blue')
plt.title('Returns of Natural Gas Futures (NG=F)')
plt.xlabel('Date')
plt.ylabel('Returns')
plt.show()

plt.plot(vol_20_NG, color='red', label='Natural Gas Volatility')
plt.plot(vol_20_SPY, color='blue', label='SPY Volatility')
plt.title('Natural Gas vs. SPY Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()

plt.scatter(cluster_0_days.index, cluster_0_days['Close'], color='green', label='Calm', s=10)
plt.scatter(cluster_1_days.index, cluster_1_days['Close'], color='orange', label='Extreme Positive', s=10)
plt.scatter(cluster_2_days.index, cluster_2_days['Close'], color='red', label='Stress', s=10)
plt.title('Natural Gas Price, Colored by Regime Cluster')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()