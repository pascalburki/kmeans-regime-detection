Good, let's find a middle ground — fuller than the ultra-compressed version, but still consistent with Regime Instability's rhythm (which does include real reasoning lines, just kept tight).
K-Means Progress Log — Fuller Version
July 25 2026
Compared K-means regimes against original rule-based regimes (2 features: returns + volatility)
Overlap: 656/1489 days (44.1%)
Key finding: methods disagree because rule-based only looks at volatility, while K-means also factors in the actual return on a given day
Script: method_comparison/july25_kmeans_vs_rulebased.py
July 26 2026
Found the most extreme disagreement day: Nov 26, 2021, a -2.26% single-day return tied to the Omicron variant shock
Rule-based called it low volatility, since the surrounding month was calm; K-means correctly flagged it as a distinct, high-stress day
Script: method_comparison/july26_disagreement_analysis.py
July 29 2026
Added correlation as a third feature (20-day rolling correlation, SPY/QQQ)
Hypothesized disagreement days would show elevated correlation, tying to the Regime Instability project's stress finding. Checked directly rather than assuming it
Disagreement days showed lower correlation (0.707 vs. 0.912 avg) and lower volatility (0.0057 vs. 0.0108 avg), the opposite of the hypothesis
Key finding: correlation adds a genuinely separate axis of regime information, not just a confirmation of the volatility signal
Script: method_comparison/july29_add_correlation_feature.py
July 30 2026
Tested rolling windows (10, 20, 60 days) and a different asset pair (SPY/GLD instead of SPY/QQQ)
Key finding: shorter windows are noisier, since a short volatile stretch dominates the whole window instead of being diluted by calm days around it
SPY/GLD produced no sharp outlier cluster, unlike SPY/QQQ, since gold moves largely independently of SPY regardless of regime, weakening correlation as a distinguishing feature for that pair
Scripts: method_comparison/july30_rolling_window_test.py, july30_different_asset_test.py
July 31 2026
Pivoted to real energy data: Natural Gas Futures (NG=F), 2018-2023, same K-means approach
Cluster sizes: 932 (calm), 293 (extreme positive), 265 (stress)
Natural gas volatility runs roughly 3-5x higher than SPY's on average
Hypothesized cluster 1 ties to the 2022 Ukraine war energy crisis. Month distribution seemed to contradict this; a year-based check confirmed it instead: 2022 had 91 days vs. 14-66 in other years
Key finding: the pattern is genuinely recurring throughout the whole period, but real crises clearly intensify it well above baseline
Script: method_comparison/july31_energy_pivot_setup.py
August 1 2026
Built a rule-based classification for natural gas, compared against K-means clusters
Cluster 0 aligns clearly with "low" (433/932 days). Clusters 1 and 2 both align most with "high," since the rule-based method can't distinguish return direction, only volatility magnitude
Grouped cluster 1's disagreement/agreement days into distinct time periods rather than treating them as isolated: 26 periods vs. "medium" (127 days), 8 periods vs. "high" (156 days)
Several periods align with known events: COVID crash, the 2022 invasion shock, the run-up to Winter Storm Uri
Repeated the analysis for cluster 2 against "high": 8 periods, 155 days, with genuinely negative returns, confirming cluster 2 captures sustained negative pressure during the same crises, distinct from cluster 1's positive spikes
Script: method_comparison/august1_energy_vs_rulebased.py
August 2 2026
Implemented HMM (Hidden Markov Model) on natural gas data, compared directly against K-means in the same script
HMM switches states only 25 times across the full period; K-means switches 656 times
Key finding: HMM's persistence modeling produces far smoother, more realistic regime assignments than K-means's day-by-day approach
Tested the previously unexplained May-Oct 2023 period directly: HMM classified all 91 corresponding days as a single hidden state, agreeing with K-means's original finding. Since HMM explicitly penalizes frequent switching, this cross-method agreement is real evidence the 2023 period was a genuine, sustained event
Script: method_comparison/august2_hmm_implementation.py
