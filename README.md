# K-Means Market Regime Detection

## Summary

This project tests whether unsupervised machine learning (K-means clustering) can identify market regimes directly from data, without manually setting thresholds. It's a direct follow-up to my Regime Instability Analysis project, which defined regimes using manually-set volatility percentiles. Here, K-means is given raw features (returns, volatility, and cross-asset correlation) and left to find its own groupings, then those groupings are compared against the manual, rule-based method.

## Assets & Data

SPY, QQQ, daily data, 2018-2023 (1,489 trading days after cleaning).

## Methodology

**Features:** daily log returns, 20-day rolling volatility, and 20-day rolling correlation between SPY and QQQ (added July 29).

**Clustering:** K-means with K=3, validated using the elbow method (tested K=2 through K=5; inertia improvement drops off sharply after K=3, from a 0.06 improvement between K=2 and K=3 down to 0.03 between K=4 and K=5).

**Comparison method:** a rule-based classification using 20-day volatility percentiles (bottom 30% = low, middle 40% = medium, top 30% = high), compared against K-means cluster assignments using a crosstab and best one-to-one label matching.

## Key Findings

**Baseline comparison (2 features: returns + volatility):** K-means and the rule-based method agree on 656 of 1,489 days (44.1% overlap). The two methods disagree because the rule-based method only looks at volatility, while K-means also factors in the actual return on a given day — so a single sharp negative-return day can get pulled into K-means' "crash" cluster even when the surrounding 20-day window was otherwise calm.

**Most extreme disagreement example:** November 26, 2021 — a -2.26% single-day return tied to the Omicron variant news shock, classified as "low volatility" by the rule-based method (since the surrounding month was calm) but correctly flagged as a distinct, high-stress day by K-means.

**Adding correlation as a third feature (July 29):** initially hypothesized that new disagreement days would show elevated correlation, tying to the Regime Instability project's core finding that correlation spikes during stress. This was checked directly rather than assumed — the data showed the opposite. Disagreement days had *lower* average correlation (0.707) and *lower* average volatility (0.0057) than the dataset average (0.912 and 0.0108, respectively). This suggests correlation captures a genuinely separate axis of regime information — identifying periods of unusually low co-movement between SPY and QQQ — rather than simply reinforcing the volatility signal.

## Status / In Progress

- Testing different rolling windows and assets to find where the model's regime assignments become unstable (in progress)
- Pivoting the methodology to real energy market data (planned)
- Adding a Hidden Markov Model as a second detection method, to compare against K-means clustering (planned)
- Building a simple regime-based trading strategy and backtesting it against historical data (planned)
- Combining this project with Regime Instability Analysis into a single dashboard (see companion repository, in progress)

## Related Work

This project builds directly on [Regime-Based Risk Instability in Financial Markets](https://github.com/pascalburki/regime-risk-instability), which defines regimes using manually-set volatility thresholds and identifies correlation, not volatility alone, as the primary driver of diversification failure under stress.
