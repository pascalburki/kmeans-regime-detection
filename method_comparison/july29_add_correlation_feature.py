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
SPY_vol = SPY_returns.rolling(window=20).std().dropna()
QQQ_returns = np.log(close_QQQ/close_QQQ.shift(1)).dropna()
QQQ_vol = QQQ_returns.rolling(window=20).std().dropna()
corr = SPY_returns.rolling(window=20).corr(QQQ_returns)

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

print("labels; ", labels)
print("lenght: ", len(labels))
print("shape: ", labels.shape)
print("Cluster value counts:", SPY_df_clean['cluster'].value_counts())
print("Cluster averages (returns, vol):", SPY_df_clean.groupby('cluster')[['returns', 'vol']].mean())

k_values = [2,3,4,5]
inertia = []

for k in k_values:
  KM = KMeans(n_clusters=k, random_state=3)
  KM = KM.fit(x)
  i = KM.inertia_
  inertia.append(i)

print("Inertia by K:", inertia)

low_cutoff = SPY_df_clean['vol'].quantile(0.30)
high_cutoff = SPY_df_clean['vol'].quantile(0.70)

SPY_df_clean['rule_regime'] = pd.cut(SPY_df_clean['vol'], bins=[-float('inf'), low_cutoff, high_cutoff, float('inf')],labels=['low', 'medium', 'high'])

print("Crosstab (cluster vs rule-based regime):", pd.crosstab(SPY_df_clean['cluster'], SPY_df_clean['rule_regime']))

cluster_to_label = {0: 'low', 1: 'medium', 2: 'high'}
SPY_df_clean['cluster_label'] = SPY_df_clean['cluster'].map(cluster_to_label)

SPY_df_clean['disagree'] = SPY_df_clean['cluster_label'] != SPY_df_clean['rule_regime']

extreme_disagreement = SPY_df_clean[(SPY_df_clean['rule_regime'] == 'low') & (SPY_df_clean['cluster_label'] == 'high')]
print("disagreements: ", extreme_disagreement.index)
print(extreme_disagreement[['returns', 'vol', 'corr']])
print("Mean correlation for extreme disagreements:", extreme_disagreement['corr'].mean())
print("Mean correlation for all data:", SPY_df_clean['corr'].mean())
print("Mean vol for disagreements:", extreme_disagreement['vol'].mean())
print("Mean vol for all data:", SPY_df_clean['vol'].mean())

plt.plot(k_values, inertia)
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

plt.scatter(x=SPY_df_clean['returns'], y=SPY_df_clean['vol'], c=SPY_df_clean['cluster'])
plt.xlabel('returns')
plt.ylabel('vol')
plt.title('scatterplot with 3 clusters')
plt.colorbar()
plt.show()

plt.scatter(x=SPY_df_clean['cluster'].index, y=SPY_df_clean['returns'], c=SPY_df_clean['cluster'])
plt.xlabel('date')
plt.ylabel('returns')
plt.title('timeview')
plt.colorbar()
plt.show()

plt.scatter(x=SPY_df_clean['rule_regime'].index, y=SPY_df_clean['returns'], c=SPY_df_clean['rule_regime'].cat.codes)
plt.xlabel('date')
plt.ylabel('returns')
plt.title('timeview')
plt.colorbar()
plt.show()