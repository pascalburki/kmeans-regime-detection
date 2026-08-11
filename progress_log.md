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
**Verified result (rerun, confirmed scaled):** cluster sizes 1024 / 29 / 436. Cluster 0: near-zero return, low vol (returns -0.0041, vol 0.0088). Cluster 1: negative return, highest vol — the stress cluster (returns -0.0073, vol 0.0490). Cluster 2: positive return, low-moderate vol (returns 0.0115, vol 0.0131)
Script: first_implementation/july11_first_kmeans_run.py
*(This matches the July 26 corrected baseline exactly, as expected — same two features, same date range, same random_state. An earlier version of this entry cited 1005/306/178 from an unscaled run; that number no longer applies to the saved script, which already includes StandardScaler.)*

## July 12
Learned the elbow method conceptually, tested K=2 through K=5
**Verified result (rerun, confirmed scaled):** Inertia: K=2: 2121.39, K=3: 1583.56, K=4: 1275.94, K=5: 856.61
Best K is 3: biggest single-step improvement happens between K=2 and K=3, then progressively smaller drops, consistent with the original interpretation
Script: first_implementation/july12_elbow_method.py
*(An earlier version of this entry cited pre-fix inertia values (0.2135/0.1508/0.1181/0.0934) from an unscaled run; those no longer apply to the saved script.)*

## July 18
Re-ran K-means (K=3), plotted returns vs. volatility scatter, color-coded by cluster
Cluster 0: lowest volatility, near-zero returns. Cluster 1: elevated volatility, best returns. Cluster 2: elevated volatility, worst returns
Script: visualization/july18_cluster_plots.py

## July 19
Plotted regime assignment over time (returns vs. date, colored by cluster) for better readability than the scatter view
**Verified result (rerun, confirmed scaled):** cluster sizes 1024 / 29 / 436 — matches July 26's baseline exactly (same features, same date range, same random_state), as expected. Inertia: 2121.39 / 1583.56 / 1275.94 / 856.61, also matching.
COVID (early-mid 2020) shows the most extreme swings in both directions across the whole 2018-2023 range
Cluster 0 (calm) forms a dense, near-continuous band; clusters 1/2 recur periodically across all years, with a secondary, smaller spike around 2022, likely tied to energy prices and rate hikes
Script: visualization/july19_regime_timeline.py
*(An earlier version of this entry flagged this script as missing StandardScaler. It has since been added and the fix is confirmed by direct rerun above — the COVID/2022 timeline observations are verified, not just carried over from before.)*

## July 25
Built a rule-based classification using volatility percentiles (bottom 30% low, middle 40% medium, top 30% high)
Compared against K-means using a crosstab; best one-to-one matching gives 656/1489 days agreeing (44.1% overlap)
Key finding: methods disagree because the rule-based method only uses volatility, while K-means also factors in returns, so a medium-volatility day with a strongly negative return gets pulled into K-means's crash cluster even though the rule-based method would call it medium
Script: method_comparison/july25_kmeans_vs_rulebased.py

## July 26
Pulled the 10 dates with the most extreme disagreement (rule-based says low, K-means says high)
*Original finding (retracted, see August 11 entry below): all 10 showed a sharp single-day negative return (-1.3% to -2.3%) paired with genuinely low 20-day volatility, most extreme case Nov 26, 2021 tied to the Omicron shock. This was an artifact of a hardcoded cluster-label bug, not a real result. The corrected version of this script returns zero disagreement days.*
Script: method_comparison/july26_disagreement_analysis.py

## July 29
Added a third feature, 20-day rolling correlation between SPY and QQQ, to the K-means input
*Original finding (retracted, see August 11 entry below): cluster sizes 461/940/88; hypothesized disagreement days would show elevated correlation, but checked directly and found mean correlation for disagreements was 0.7073 vs. 0.9125 overall — the opposite of the hypothesis. Both the cluster sizes and the disagreement analysis were invalidated by the unscaled-feature bug and a separate hardcoded-label bug.*
**Verified result (rerun, confirmed scaled):** cluster sizes 371 / 30 / 1088. Cluster 1 is a sharp 30-day high-vol outlier (mean vol 0.0489), cleanly separated from cluster 0 (371 days, vol 0.0065) and cluster 2 (1088 days, vol 0.0113). Derived cluster-to-label mapping (ranked by mean vol): {0: low, 2: medium, 1: high}. With correct labels, the "low vol but high cluster" disagreement category is empty — zero matching days — confirming the retraction above rather than just asserting it.
Script: method_comparison/july29_add_correlation_feature.py

## July 30
Tested rolling window size (10, 20, 60 days) and a different asset pair (SPY/GLD instead of SPY/QQQ)
*Original findings (retracted, see August 11 entry below): both were affected by the unscaled-feature bug.*
Scripts: method_comparison/july30_rolling_window_test.py, july30_different_asset_test.py

**Verified result (rerun, rolling-window test, confirmed scaled):**
- 10-day window: cluster sizes **1005 / 187 / 307** (1499 total days). Cluster 0: returns -0.0034, vol 0.0089. Cluster 1: returns 0.0021, vol 0.0058 (lowest vol). Cluster 2: returns 0.0119, vol 0.0187 (highest vol/return, 307 days — no sharp small outlier).
- 20-day window: cluster sizes **371 / 30 / 1088** (1489 total days). Cluster 1 is a sharp 30-day high-vol outlier (vol 0.0489).
- 60-day window: cluster sizes **599 / 64 / 786** (1449 total days). Cluster 1 is a sharp 64-day high-vol/high-return outlier (returns 0.0065, vol 0.0358).

Key finding (holds up): shorter windows are noisier and don't isolate a clean, sharply-separated outlier regime — the 10-day case's most volatile group is 307 days (20% of the data) with no small extreme cluster, while the 20-day and 60-day windows both carve out a small, sharply distinct high-vol group (30 and 64 days respectively). The *specific* cluster sizes previously logged for the 10-day and 60-day cases (417/120/962 and 196/708/545) did not match this rerun and have been replaced — only the 20-day figure (371/30/1088) was ever actually verified before. The qualitative conclusion about window length and noise is unaffected.

**Verified result (rerun, SPY/GLD asset comparison, confirmed scaled):** cluster sizes 863 / 594 / 32. Cluster 2 (mean vol 0.048) is an outlier cluster nearly identical in size and severity to SPY/QQQ's (30-32 days, vol ~0.048-0.049 in both cases). The original claim that "SPY/GLD produces three evenly-sized clusters with no outlier group" is false and is retracted — this was an artifact of the unscaled-feature bug, not a real property of the asset pair.

## July 31
Pivoted to real energy data: Natural Gas Futures (NG=F), 2018-2023, same K-means approach
**Verified result (rerun, confirmed scaled):** cluster sizes 799 (cluster 0) / 317 (cluster 1) / 374 (cluster 2)
- Cluster 0: returns -0.0012, vol 0.0241 — calm/neutral
- Cluster 1: returns **-0.0497**, vol 0.0552 — this is the **stress** cluster (sharp negative, highest vol), concentrated in 2022 (101 days) and 2020 (61 days)
- Cluster 2: returns **+0.0440**, vol 0.0511 — this is the **extreme positive** cluster, also concentrated in 2022 (114 days) and 2020 (81 days)

Natural gas volatility runs roughly 3-5x higher than SPY's on average. Cluster 1 (stress) and cluster 2 (positive) are both genuinely recurring patterns throughout the whole period, but 2022 (Ukraine war energy crisis) and 2020 (COVID) clearly amplify their frequency well above baseline.
Script: method_comparison/july31_energy_pivot_setup.py

*An earlier version of this entry cited cluster sizes 932/293/265. That number does not correspond to any verified run of the current script and has been removed — 799/317/374 is the only confirmed figure (rerun and directly verified from script output). Root cause of the discrepancy could not be determined: there is no earlier saved version of this script that produces 932/293/265, and no change to the date range or data source was identified that would explain it. Flagging this honestly rather than guessing at a cause that can't be confirmed.*

**✅ Bug found and fixed:** the plot legend in this script had cluster 1 and cluster 2 swapped (labeled `cluster_1_days` as "Extreme Positive" and `cluster_2_days` as "Stress", when the means show it's the other way around). Same hardcoded-index pattern as Bug 2 below. Fixed by swapping the legend labels.

## August 1
Compared K-means against a rule-based classification for natural gas, using dynamically-derived cluster labels (fix for Bug 2, see below) instead of assuming a fixed cluster-to-label mapping
Cluster means confirm: cluster 2 = extreme positive (mean return 0.044), cluster 1 = extreme negative (mean return -0.050), cluster 0 = neutral
Grouped disagreement/agreement days into distinct time periods instead of treating them in isolation:
- 147 days across 20 periods where K-means called a day "extreme positive" but the rule-based method called it "medium"
- 217 days across 10 periods where K-means called a day "extreme negative" but rule-based called it "high"
Several periods match known events: Nov 2018-Feb 2019, the 2020 COVID crash window, the Oct 2021-Mar 2022 run-up to the Ukraine invasion, and a long Oct 2022-May 2023 stretch (208 days) that remains only partially explained
Script: method_comparison/august1_energy_vs_rulebased.py

## August 2
Dedicated teaching session on Hidden Markov Models: hidden states, transition probabilities, and how HMM differs from K-means by modeling sequence and persistence rather than treating each day independently
Implemented HMM on the same natural gas data (with StandardScaler applied)
**Verified result:** hidden state sizes 605 / 20 / 865, HMM switches: 16, K-means switches on the same scaled data: 536
Tested the previously-unexplained Oct 2022-May 2023 period directly: HMM classified all corresponding days as one hidden state, agreeing with K-means. Since HMM penalizes frequent switching, this cross-method agreement is real evidence the period was a genuine, sustained event, not noise
Script: august2_hmm_implementation.py

*Note: an earlier draft of this entry cited "K-means switches: 656" — on inspection, 656 was a copy error, not a genuine K-means switch count. It's actually the July 25 crosstab agreement figure (656/1489 days). The real K-means switch count, computed directly in the script, is 536.*

---

## Bugs found and fixed (summary)

**Bug 1: unscaled features.** K-means clusters using raw Euclidean distance. Correlation (range roughly -1 to 1) is on a much bigger numeric scale than returns or volatility (both roughly 0.001-0.05), so before scaling, correlation was silently dominating every distance calculation. Fixed by adding `StandardScaler` before every `KMeans.fit()` call, before the elbow-method loop, and before `GaussianHMM.fit()`.
- Affected and fixed, verified by direct rerun with printed output: July 26, July 29, both July 30 scripts, August 2, July 31, July 11, July 12, July 19.
- Confirmed clean from the start (already had StandardScaler, verified by direct rerun): July 18, July 25.

**Bug 1 status: fully resolved.** Every script in this project now uses StandardScaler and has been verified by direct rerun.

**Bug 2: hardcoded cluster-to-label mapping.** Several scripts assumed a fixed mapping like `{0: 'low', 1: 'medium', 2: 'high'}` based on cluster number, but K-means assigns cluster numbers arbitrarily on each fit. This mapping went stale once the scaling fix changed cluster composition. Fixed in July 26, July 29, and August 1 by deriving the mapping from actual per-cluster statistics (mean volatility or mean return, ranked) on every run.
- July 31's plot legend swap: fixed (see July 31 entry above — same hardcoded-index pattern as Bug 2, in a plot legend rather than a filtering condition).

**General lesson:** both bugs produced plausible-looking, coherent results with no errors or crashes — the kind of bug that's easy to miss because nothing looks broken. Cluster number-to-meaning mappings should be treated as arbitrary per run going forward, and feature scaling should be checked before trusting any cluster-composition-based finding.

**Separate lesson (not a code bug, a record-keeping one):** two logged figures — July 31's original cluster sizes (932/293/265) and July 30's 10-day/60-day rolling-window sizes (417/120/962 and 196/708/545) — turned out not to correspond to any actual script run once rechecked directly. In both cases the totals happened to add up correctly, which is likely why it went unnoticed. Where the root cause could be identified, it's noted above; where it couldn't (July 31), that's stated plainly rather than guessed at. Numbers that are stated but never re-verified against fresh script output are a real risk in a fast-moving log like this one; worth spot-checking a rerun periodically rather than assuming a recorded figure is still current.

**Open items going into the next session:** none — all known code bugs are fixed and verified by direct rerun.
