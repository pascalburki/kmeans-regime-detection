# K-Means Market Regime Detection

## Summary

This project tests whether unsupervised machine learning (K-means clustering) can identify market regimes directly from data, without manually setting thresholds. It's a direct follow-up to my Regime Instability Analysis project, which defined regimes using manually-set volatility percentiles.

K-means is given raw features (returns, volatility, and cross-asset correlation) and left to find its own groupings, compared against a manual, rule-based method. Later extended to real energy market data and to a Hidden Markov Model, to address a real limitation K-means has: no memory of time.

**A note on process:** this project went through two rounds of real bug-fixing — unscaled features letting correlation dominate the clustering, and a hardcoded cluster-to-label mapping that went stale once cluster composition changed. Several early findings were revised or retracted as a result. Everything below reflects the corrected, verified state — every script in the project has been fixed and re-verified by direct rerun. The full history — what was originally found, what turned out to be wrong, and why — is documented in `progress_log.md` for anyone who wants the complete record.

## Assets & Data

SPY, QQQ — daily data, 2018-2023 (1,489 trading days after cleaning), equity baseline.

NG=F (Natural Gas Futures) — daily data, 2018-2023, energy pivot.

GLD — daily data, 2018-2023, used for a cross-asset correlation comparison.

## Methodology

Features: daily log returns, 20-day rolling volatility, and (where noted) 20-day rolling correlation between two assets. All features are standardized (`StandardScaler`) before clustering, so no single feature dominates the distance calculation purely due to its numeric scale.

Clustering: K-means with K=3, validated using the elbow method (K=2 through K=5).

Comparison method: a rule-based classification using 20-day volatility percentiles (bottom 30% = low, middle 40% = medium, top 30% = high), compared against K-means cluster assignments via crosstab. Cluster-to-label mappings are derived dynamically from each run's actual cluster statistics (ranked mean volatility or mean return), not assumed — K-means cluster numbers are arbitrary and can't be hardcoded to a meaning.

HMM: a Gaussian Hidden Markov Model with 3 hidden states, fit on the same standardized features, compared directly against K-means.

## Key Findings

**Baseline (returns + volatility, SPY):** K-means produces cluster sizes 1024 / 29 / 436. The 29-day cluster is a sharply distinct stress regime (mean return -0.007, mean vol 0.049) — cleanly separated from calm (1024 days, near-zero return) and moderate-positive (436 days) regimes.

**Elbow method:** inertia drops from 2121 (K=2) to 1584 (K=3) to 1276 (K=4) to 857 (K=5) — the largest single-step improvement is between K=2 and K=3, supporting K=3 as the right choice.

**Adding correlation as a third feature (SPY/QQQ):** cluster sizes 371 / 30 / 1088, with the same kind of sharp 30-day high-volatility outlier (mean vol 0.049) as the baseline.

**Window length sensitivity:** a 10-day window produces no small, sharp outlier cluster at all (largest high-vol group is 307 days, 20% of the data) — genuinely noisier and less separated than the 20-day (30-day outlier) or 60-day (64-day outlier) windows. Shorter windows dilute the signal.

**Cross-asset comparison (SPY/GLD vs. SPY/QQQ):** both asset pairs produce a nearly identical small, sharp outlier cluster (30-32 days, vol ~0.048-0.049) once features are properly scaled. There's no evidence in this project that a more-correlated second asset changes regime separability.

**Energy pivot (NG=F):** cluster sizes 799 / 317 / 374. Cluster 1 (mean return -0.050, mean vol 0.055) is the stress regime; cluster 2 (mean return 0.044, mean vol 0.051) is an extreme-positive regime. Both concentrate heavily in 2022 (101 and 114 days respectively) and 2020 (61 and 81 days) — consistent with the Ukraine energy crisis and COVID.

**Energy vs. rule-based comparison:** grouping disagreement days into contiguous periods rather than treating them as isolated dates reveals real structure — 147 days across 20 periods where K-means called "extreme positive" but the rule-based method called "medium," and 217 days across 10 periods for the negative/high case. Several periods line up with known events: the Nov 2018-Feb 2019 stretch, the 2020 COVID crash, the run-up to the Ukraine invasion (Oct 2021-Mar 2022), and a long Oct 2022-May 2023 stretch that remains only partially explained.

**Adding HMM:** hidden state sizes 605/20/865 on NG=F, with only 16 regime switches versus K-means's 536 switches on the same standardized data. HMM's persistence-based structure produces far fewer switches, consistent with it modeling time-dependence directly rather than treating each day independently.

## Limitations

Window length materially affects cluster separation — shorter windows are noisier.

No evidence found that correlation strength between assets changes regime separability (tested on SPY/QQQ and SPY/GLD).

HMM requires more assumptions than K-means (transition probability estimation, initialization sensitivity).

The two bugs described in the process note above (unscaled features, hardcoded cluster labels) both produced plausible-looking, coherent results with no errors or crashes — exactly the kind of bug that's easy to miss because nothing looks broken. Any future extension of this project should treat cluster numbers as arbitrary per-run and verify feature scaling before drawing conclusions from cluster composition.

## Status

Core analysis complete. All known bugs fixed and verified by direct rerun — nothing currently open.

Next: incorporated into the combined Regime Strategy Dashboard (separate repo).

## Related Work

This project builds directly on [Regime-Based Risk Instability in Financial Markets](https://github.com/pascalburki/regime-risk-instability), which defines regimes using manually-set volatility thresholds and identifies correlation, not volatility alone, as the primary driver of diversification failure under stress.