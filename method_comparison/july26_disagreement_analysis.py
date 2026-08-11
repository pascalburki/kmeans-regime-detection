import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x_scaled)
df_clean['cluster'] = labels

print("labels; ", labels)
print("lenght: ", len(labels))
print("shape: ", labels.shape)
print("Cluster value counts:", df_clean['cluster'].value_counts())
print("Cluster averages (returns, vol_20):", df_clean.groupby('cluster')[['returns', 'vol_20']].mean())

k_values = [2,3,4,5]
inertia = []

for k in k_values:
  KM = KMeans(n_clusters=k, random_state=3)
  KM = KM.fit(x_scaled)
  i = KM.inertia_
  inertia.append(i)

print("Inertia by K:", inertia)

low_cutoff = df_clean['vol_20'].quantile(0.30)
high_cutoff = df_clean['vol_20'].quantile(0.70)

df_clean['rule_regime'] = pd.cut(df_clean['vol_20'], bins=[-float('inf'), low_cutoff, high_cutoff, float('inf')],labels=['low', 'medium', 'high'])

print("Crosstab (cluster vs rule-based regime):", pd.crosstab(df_clean['cluster'], df_clean['rule_regime']))

# --- NEW: derive cluster meaning from actual data instead of assuming {0:'low',1:'medium',2:'high'} ---
vol_ranking = df_clean.groupby('cluster')['vol_20'].mean().sort_values()
print("\nCluster volatility ranking (lowest to highest):")
print(vol_ranking)
cluster_to_label = {cluster: label for cluster, label in zip(vol_ranking.index, ['low', 'medium', 'high'])}
print(f"Derived cluster_to_label mapping: {cluster_to_label}")

df_clean['cluster_label'] = df_clean['cluster'].map(cluster_to_label)

df_clean['disagree'] = df_clean['cluster_label'] != df_clean['rule_regime']

extreme_disagreement = df_clean[(df_clean['rule_regime'] == 'low') & (df_clean['cluster_label'] == 'high')]
print("disagreements: ", extreme_disagreement.index)
print(extreme_disagreement[['returns', 'vol_20']])

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

plt.scatter(x=df_clean['cluster'].index, y=df_clean['returns'], c=df_clean['cluster'])
plt.xlabel('date')
plt.ylabel('returns')
plt.title('timeview')
plt.colorbar()
plt.show()

plt.scatter(x=df_clean['rule_regime'].index, y=df_clean['returns'], c=df_clean['rule_regime'].cat.codes)
plt.xlabel('date')
plt.ylabel('returns')
plt.title('timeview')
plt.colorbar()
plt.show()
