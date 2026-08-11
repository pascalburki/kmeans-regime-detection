import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = yf.download('NG=F', '2018-01-01', '2023-12-31')
df.columns = df.columns.get_level_values(0) 

close = df["Close"]
returns = np.log(close/close.shift(1)).dropna()
vol = returns.rolling(window=20).std().dropna()

df["returns"] = returns
df["vol"] = vol
df_clean = df.dropna().copy()
x = df_clean[['returns', 'vol']]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x_scaled)
df_clean['cluster'] = labels

# --- NEW: figure out which cluster number actually means what, instead of assuming ---
cluster_means = df_clean.groupby('cluster')[['returns', 'vol']].mean()
print("Cluster means (check this before trusting any 'cluster == N' logic):")
print(cluster_means)

# Rank clusters by mean return: lowest = most negative, highest = most positive
return_ranking = cluster_means['returns'].sort_values()
cluster_negative = return_ranking.index[0]   # most negative returns
cluster_neutral  = return_ranking.index[1]   # middle
cluster_positive = return_ranking.index[2]   # most positive returns

print(f"\nCluster {cluster_positive} = extreme positive (highest mean return)")
print(f"Cluster {cluster_neutral} = neutral/calm")
print(f"Cluster {cluster_negative} = extreme negative (lowest mean return)")

top_30 = df_clean['vol'].quantile(0.70)
bottom_30 = df_clean['vol'].quantile(0.30)

df_clean['rule_regime'] = pd.cut(df_clean['vol'], bins=[-float('inf'), bottom_30, top_30, float('inf')], labels=['low', 'medium', 'high'])

# --- CHANGED: use cluster_positive instead of hardcoded 1 ---
disagreement_medium = df_clean[(df_clean['cluster'] == cluster_positive) & (df_clean['rule_regime'] == 'medium')]
disagreement_dates_medium = disagreement_medium.index.sort_values()

# --- CHANGED: use cluster_negative instead of hardcoded 2, since "high vol + negative return" is the stress cluster ---
disagreement_high = df_clean[(df_clean['cluster'] == cluster_negative) & (df_clean['rule_regime'] == 'high')]
disagreement_dates_high = disagreement_high.index.sort_values()

periods_medium = []
current_period_start_medium = disagreement_dates_medium[0]
current_period_end_medium = disagreement_dates_medium[0]

periods_high = []
current_period_start_high = disagreement_dates_high[0]
current_period_end_high = disagreement_dates_high[0]

for date in disagreement_dates_medium[1:]:
    if (date - current_period_end_medium).days <= 14:
        current_period_end_medium = date
    else:
        periods_medium.append((current_period_start_medium, current_period_end_medium))
        current_period_start_medium = date
        current_period_end_medium = date

periods_medium.append((current_period_start_medium, current_period_end_medium))

for date in disagreement_dates_high[1:]:
    if (date - current_period_end_high).days <= 14:
        current_period_end_high = date
    else:
        periods_high.append((current_period_start_high, current_period_end_high))
        current_period_start_high = date
        current_period_end_high = date

periods_high.append((current_period_start_high, current_period_end_high))

print("\ncomparison of KMeans clusters and rule-based regimes: ")
print(pd.crosstab(df_clean['cluster'], df_clean['rule_regime']))
print(f"Total days where cluster={cluster_positive} (positive) but rule_regime='medium':", len(disagreement_medium))
print(f"Cluster {cluster_positive} (extreme positive) days that rule-based calls 'medium':", disagreement_medium[['returns', 'vol']].sort_values('returns', ascending=False).head(10))
print(f"number of periods: , {len(periods_medium)}")
for start, end in periods_medium:
    print(f"period: {start} to {end}, length: {(end - start).days} days")

print(f"\nTotal days where cluster={cluster_negative} (negative) but rule_regime='high':", len(disagreement_high))
print(f"Cluster {cluster_negative} (extreme negative) days that rule-based calls 'high':", disagreement_high[['returns', 'vol']].sort_values('returns', ascending=True).head(10))
print(f"number of periods: , {len(periods_high)}")
for start, end in periods_high:
    print(f"period: {start} to {end}, length: {(end - start).days} days")