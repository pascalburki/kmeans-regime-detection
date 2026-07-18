import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans 
import yfinance as yf

df_SPY = yf.download('SPY', '2018-01-01', '2023-12-31')
df_SPY.columns = df_SPY.columns.get_level_values(0)

close = df_SPY["Close"]
returns = np.log(close/close.shift(1)).dropna()
vol_20 = returns.rolling(window=20).std().dropna()

df_SPY['returns']=returns
df_SPY['vol_20']=vol_20

df_clean = df_SPY.dropna().copy()
x = df_clean[['returns', 'vol_20']]
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x)
df_clean['cluster'] = labels

print("labels; ", labels)
print("lenght: ", len(labels))
print("shape: ", labels.shape)
print(df_clean['cluster'].value_counts())
print(df_clean.groupby('cluster')[['returns', 'vol_20']].mean())

k_values = [2,3,4,5]
inertia = []

for k in k_values:
  KM = KMeans(n_clusters=k, random_state=3)
  KM = KM.fit(x)
  i = KM.inertia_
  inertia.append(i)

print("inertia: ", inertia)

plt.plot(k_values, inertia)
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

plt.scatter(x=df_clean['returns'], y=df_clean['vol_20'], c=df_clean['cluster'])
plt.xlabel('returns')
plt.ylabel('vol_20')
plt.title('scatterplot with 3 clusters')
plt.colorbar()
plt.show()
