## July 4 2026
Learned K-means conceptually: clusters, centroids, distance
Worked through distance calculations and centroid updates by hand on toy points
Key finding: K-means works by grouping points together based on their distance 
to the nearest centroid. Each point gets assigned to whichever centroid is 
closest, then the centroid moves to the center of its group, and this process 
repeats until the centroids don't move anymore.

## July 5 2026
Set up new repo: kmeans-regime-detection
Pulled SPY price data 2018-2023
Computed log returns and 20-day rolling volatility
Key finding: my input features are daily returns and rolling 20 day volatility. returns show the direction and size of price moves, and volatility shows how calm or chaotic
the period was, together they can help us see regimes 
Script: foundations/july5_data_setup.py

## July 11 2026
Ran first K-means clustering (K=3) on SPY returns + 20-day volatility, 2018-2023
Cluster sizes: 0 = 1005 days, 1 = 306 days, 2 = 178 days
Cluster 0: near-zero return, lowest vol
Cluster 1: strong positive return, moderate-high vol
Cluster 2: strong negative return, highest vol
Script: first_implementation/july11_first_kmeans_run.py

## July 12 2026
Learned elbow method conceptually
Tested K=2 through K=5, plotted inertia curve
Inertia: K=2: 0.2135, K=3: 0.1508, K=4: 0.1181, K=5: 0.0934
Best K appears to be 3 because it has the biggest improvement, and after that 
diminishing returns start, 0.06 improvement from 2 to 3, then 0.04, then 0.03
Script: first_implementation/july12_elbow_method.py

## July 18 2026
Re-ran K-means with K=3 on SPY returns + 20-day volatility
Plotted returns vs volatility scatter, color-coded by cluster
Cluster 0 represents the lowest volatility with near 0 returns
Cluster 1 represents elevated volatility with the best returns
Cluster 2 represents elevated volatility with the worst returns
Script: visualization/july18_cluster_plots.py

## July 19 2026
Plotted regime assignment over time, switched from cluster vs date scatter 
to returns vs date scatter (colored by cluster) for better readability
Confirmed average return/volatility per regime from July 11 groupby
COVID (early to mid 2020) shows the most extreme swings in both directions, 
largest single drop and largest single spike in the whole 2018 to 2023 range
Cluster 0 (calm) forms a dense, near continuous band throughout, rarely 
interrupted
Clusters 1/2 (rally/crash) recur periodically across all years, not just 
2020, with a secondary smaller spike of activity around 2022
Regime behavior suggests that the most volatile period was mid 2020 during 
COVID, with a secondary but smaller period of elevated volatility in 2022, 
likely tied to energy price shocks and rate hikes
Script: visualization/july19_regime_timeline.py

## July 25 2026
Built rule based regime classification using vol_20 percentiles (bottom 30 
percent low, middle 40 percent medium, top 30 percent high)
Compared against K means cluster assignments using pd.crosstab
Crosstab results:
cluster 0: low 424, medium 413, high 168
cluster 1: low 13, medium 123, high 170
cluster 2: low 10, medium 59, high 109
Best one to one matching: cluster 0 to low, cluster 1 to medium, cluster 2 
to high, giving 656 out of 1489 days agreeing, 44.1 percent overlap
Methods disagree because the quantile method only uses volatility to 
classify regimes, while K means uses both returns and volatility together, 
so a day with medium volatility but a strongly negative return gets pulled 
into K means high/crash cluster even though quantile method would call it 
medium based on volatility alone
Script: method_comparison/july25_kmeans_vs_rulebased.py

## July 26 2026
Mapped K means cluster numbers to rule based label names (0 to low, 1 to 
medium, 2 to high) so both methods could be compared directly
Flagged all rows where the two methods disagreed
Pulled the 10 dates with the most extreme disagreement (rule based says 
low, K means says high)
All 10 dates showed a sharp single day negative return (roughly -1.3 
percent to -2.3 percent) paired with genuinely low 20 day rolling 
volatility
Most extreme case: Nov 26 2021, return of -2.26 percent, tied to the 
Omicron variant news shock, not the COVID crash itself (which was March 
2020)
K means is better than rule based because it factors in actual daily 
returns, not just a smoothed 20 day volatility window, so it catches sharp 
single day shocks that rule based misses when the surrounding month was 
otherwise calm
Script: method_comparison/july26_disagreement_analysis.py
