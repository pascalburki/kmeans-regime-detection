import pandas as pd
import numpy as np
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
model = KMeans(n_clusters=3, random_state=3)
labels = model.fit_predict(x)
df_clean['cluster'] = labels

top_30 = df_clean['vol'].quantile(0.70)
bottom_30 = df_clean['vol'].quantile(0.30)

df_clean['rule_regime'] = pd.cut(df_clean['vol'], bins=[-float('inf'), bottom_30, top_30, float('inf')], labels=['low', 'medium', 'high'])
disagreement_medium = df_clean[(df_clean['cluster'] == 1) & (df_clean['rule_regime'] == 'medium')]
disagreement_dates_medium = disagreement_medium.index.sort_values()
disagreement_high = df_clean[(df_clean['cluster'] == 1) & (df_clean['rule_regime'] == 'high')]
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

print("comparison of KMeans clusters and rule-based regimes: ")
print(pd.crosstab(df_clean['cluster'], df_clean['rule_regime']))
print("Total days where cluster=1 but rule_regime='medium':", len(disagreement_medium))
print("Cluster 1 (extreme positive) days that rule-based calls 'medium':", disagreement_medium[['returns', 'vol']].sort_values('returns', ascending=False).head(10))
print(f"number of periods: , {len(periods_medium)}")
for start, end in periods_medium:
    print(f"period: {start} to {end}, length: {(end - start).days} days")

print("Total days where cluster=1 but rule_regime='high':", len(disagreement_high))
print("Cluster 1 (extreme positive) days that rule-based calls 'high':", disagreement_high[['returns', 'vol']].sort_values('returns', ascending=False).head(10))
print(f"number of periods: , {len(periods_high)}")
for start, end in periods_high:
    print(f"period: {start} to {end}, length: {(end - start).days} days")