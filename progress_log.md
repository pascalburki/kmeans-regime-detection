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
