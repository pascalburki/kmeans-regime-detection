## July 4
Learned K-means conceptually: clusters, centroids, distance
Worked through distance calculations and centroid updates by hand on toy points
Key finding: each point gets assigned to whichever centroid is closest, then the centroid moves to the center of its group, and this repeats until centroids stop moving
## July 5
Set up repo, pulled SPY price data 2018-2023
Computed log returns and 20-day rolling volatility
Key finding: returns show direction and size of price moves, volatility shows how calm or chaotic the period was, together they help reveal regimes
Script: data_foundation/july5_data_setup.py
## July 11
Ran first K-means clustering (K=3) on SPY returns + 20-day volatility
Cluster sizes: 0 = 1005 days, 1 = 306 days, 2 = 178 days
Cluster 0: near-zero return, lowest vol. Cluster 1: strong positive return, moderate-high vol. Cluster 2: strong negative return, highest vol
Script: first_implementation/july11_first_kmeans_run.py
## July 12
Learned the elbow method conceptually, tested K=2 through K=5
Inertia: K=2: 0.2135, K=3: 0.1508, K=4: 0.1181, K=5: 0.0934
Best K is 3: biggest improvement (0.06) happens between K=2 and K=3, then diminishing returns (0.04, then 0.03)
Script: first_implementation/july12_elbow_method.py
## July 18
Re-ran K-means (K=3), plotted returns vs. volatility scatter, color-coded by cluster
Cluster 0: lowest volatility, near-zero returns. Cluster 1: elevated volatility, best returns. Cluster 2: elevated volatility, worst returns
Script: visualization/july18_cluster_plots.py
## July 19
Plotted regime assignment over time (returns vs. date, colored by cluster) for better readability than the scatter view
COVID (early-mid 2020) shows the most extreme swings in both directions across the whole 2018-2023 range
Cluster 0 (calm) forms a dense, near-continuous band; clusters 1/2 recur periodically across all years, with a secondary, smaller spike around 2022, likely tied to energy prices and rate hikes
Script: visualization/july19_regime_timeline.py
## July 25
Built a rule-based classification using volatility percentiles (bottom 30% low, middle 40% medium, top 30% high)
Compared against K-means using a crosstab; best one-to-one matching gives 656/1489 days agreeing (44.1% overlap)
Key finding: methods disagree because the rule-based method only uses volatility, while K-means also factors in returns, so a medium-volatility day with a strongly negative return gets pulled into K-means's crash cluster even though the rule-based method would call it medium
Script: method_comparison/july25_kmeans_vs_rulebased.py
## July 26
Pulled the 10 dates with the most extreme disagreement (rule-based says low, K-means says high)
All 10 showed a sharp single-day negative return (-1.3% to -2.3%) paired with genuinely low 20-day volatility
Most extreme case: Nov 26, 2021, -2.26%, tied to the Omicron shock, not the COVID crash
Key finding: K-means is better here because it factors in actual daily returns, not just smoothed volatility, catching sharp single-day shocks that rule-based misses in an otherwise calm month
Script: method_comparison/july26_disagreement_analysis.py
## July 29
Added a third feature, 20-day rolling correlation between SPY and QQQ, to the K-means input
Cluster sizes: 461/940/88. Hypothesized disagreement days would show elevated correlation, tying to the Regime Instability project's stress finding
Checked directly instead of assuming it: mean correlation for disagreements was 0.7073 vs. 0.9125 overall, mean vol 0.0057 vs. 0.0108, both lower than average, the opposite of the hypothesis
Key finding: correlation adds a genuinely separate axis of information beyond volatility, not just a confirmation of it
Script: method_comparison/july29_add_correlation_feature.py
## July 30
Tested rolling window size (10, 20, 60 days): cluster sizes shifted meaningfully (10-day 417/120/962, 20-day 461/940/88, 60-day 196/708/545)
Key finding: shorter windows are noisier, since fewer days averaged means a short volatile stretch dominates the window instead of being diluted by calm days around it
Tested a different asset pair (SPY/GLD instead of SPY/QQQ, same 20-day window): SPY/QQQ produced one small, sharply distinct high-vol cluster (88 days), SPY/GLD produced three evenly-sized clusters with no outlier group
Key finding: the model loses sharp regime separation when the second asset isn't strongly correlated with the first during stress, since GLD moves independently of SPY regardless of regime
Scripts: method_comparison/july30_rolling_window_test.py, july30_different_asset_test.py
## July 31
Pivoted to real energy data: Natural Gas Futures (NG=F), 2018-2023, same K-means approach
Cluster sizes: 932 (calm), 293 (extreme positive), 265 (stress). Natural gas volatility runs roughly 3-5x higher than SPY's on average
Hypothesized cluster 1 ties to the 2022 Ukraine war energy crisis. Month distribution seemed to contradict this; a year-based check told a different story: 2022 had 91 days vs. 14-66 in other years, clearly elevated
Key finding: cluster 1 is a genuinely recurring pattern throughout the whole period, but real crises (2022 war, 2020 COVID) clearly amplify its frequency well above baseline
Script: method_comparison/july31_energy_pivot_setup.py
## August 1
Compared K-means against a rule-based classification for natural gas
Cluster 0 aligns clearly with "low" (433/932). Clusters 1 and 2 both align most with "high," since the rule-based method can't distinguish return direction, only volatility magnitude
Grouped disagreement/agreement days into distinct time periods instead of treating them in isolation: 26 periods vs. "medium" (127 days), 8 periods vs. "high" (156 days), several matching known events (COVID crash, 2022 invasion shock, run-up to Winter Storm Uri). One long stretch (May-Oct 2023) still unexplained
Repeated the analysis for cluster 2 against "high": 8 periods, 155 days, genuinely negative returns, confirming it captures sustained negative pressure during the same crises, distinct from cluster 1's positive spikes
Script: method_comparison/august1_energy_vs_rulebased.py
## August 2
Dedicated teaching session on Hidden Markov Models: hidden states, transition probabilities, and how HMM differs from K-means by modeling sequence and persistence rather than treating each day independently. No code written, per the plan
Implemented HMM on the same natural gas data: state sizes 604/506/380, switches only 25 times across the full period vs. K-means's 656
Tested the unexplained 2023 period directly: HMM classified all 91 corresponding days as one hidden state, agreeing with K-means. Since HMM penalizes frequent switching, this cross-method agreement is real evidence the 2023 period was a genuine, sustained event
