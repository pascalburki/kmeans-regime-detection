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
