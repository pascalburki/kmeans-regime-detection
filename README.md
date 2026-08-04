# K-Means Market Regime Detection

## Summary

This project tests whether unsupervised machine learning (K-means clustering) can identify market regimes directly from data, without manually setting thresholds. It's a direct follow-up to my Regime Instability Analysis project, which defined regimes using manually-set volatility percentiles.

K-means is given raw features (returns, volatility, and cross-asset correlation) and left to find its own groupings, compared against the manual, rule-based method. Later extended to real energy market data and to a Hidden Markov Model, to address a real limitation K-means has: no memory of time.

## Assets & Data

SPY, QQQ — daily data, 2018-2023 (1,489 trading days after cleaning), equity baseline.

NG=F (Natural Gas Futures) — daily data, 2018-2023, energy pivot.

## Methodology

Features: daily log returns, 20-day rolling volatility, and 20-day rolling correlation between SPY and QQQ (added July 29).

Clustering: K-means with K=3, validated using the elbow method (tested K=2 through K=5; inertia improvement drops off sharply after K=3, from a 0.06 improvement between K=2 and K=3 down to 0.03 between K=4 and K=5).

Comparison method: a rule-based classification using 20-day volatility percentiles (bottom 30% = low, middle 40% = medium, top 30% = high), compared against K-means cluster assignments using a crosstab and best one-to-one label matching.

HMM: a Gaussian Hidden Markov Model with 3 hidden states, fit on the same features, compared directly against K-means on the same data.

## Key Findings

Baseline comparison (2 features: returns + volatility): K-means and the rule-based method agree on 656 of 1,489 days (44.1% overlap). The two methods disagree because the rule-based method only looks at volatility, while K-means also factors in the actual return on a given day.

Most extreme disagreement example: November 26, 2021, a -2.26% single-day return tied to the Omicron variant news shock. Classified as "low volatility" by the rule-based method since the surrounding month was calm, but correctly flagged as a distinct, high-stress day by K-means.

Adding correlation as a third feature (July 29): I initially hypothesized disagreement days would show elevated correlation, tying to the Regime Instability project's core finding that correlation spikes during stress. I checked this directly instead of assuming it, and the data showed the opposite. Disagreement days had lower average correlation (0.707) and lower average volatility (0.0057) than the dataset average (0.912 and 0.0108). Correlation captures a genuinely separate axis of regime information, not just a confirmation of the volatility signal.

Energy pivot (NG=F): the same methodology applied to natural gas confirms it generalizes beyond equities. Natural gas's average volatility is roughly 3-5x higher than SPY's. A cluster of extreme single-day spikes was tested against two hypotheses, the 2022 Russia-Ukraine energy crisis and seasonal winter demand. A month-level check seemed to contradict the crisis hypothesis, but a year-level check confirmed it: 2022 had 91 such days versus 14-66 in other years.

Grouping disagreement days into periods instead of treating them as scattered individual days revealed real, identifiable events. Cluster 1 vs. rule-based "medium" gave 127 days across 26 periods, several matching the COVID crash, the post-invasion energy shock, and the run-up to Winter Storm Uri. One 129-day stretch (May-Oct 2023) didn't match an obvious single event.

Adding HMM: K-means re-evaluates every day independently, so one calmer day in the middle of a stress period causes a regime switch for that single day, then a switch back. HMM factors in the probability of staying in the same regime, and this shows up directly in the numbers: only 25 regime switches across the full 2018-2023 period, versus K-means's 656. HMM also independently confirmed the unexplained 2023 period was one genuine, persistent regime, agreeing with K-means despite using a completely different method, since HMM specifically penalizes frequent switching.

## Limitations

Window length affects results significantly. A longer rolling window smooths volatility more than a shorter one, since it averages over more days. A 20-day stress period looks highly volatile in a 20-day window, but the same period gets diluted by surrounding calm days in a 50-day window.

Correlation was only tested on one asset pair, SPY/QQQ. A different pairing, especially one with historically low or negative correlation like SPY/GLD, could behave very differently under stress, with correlation dropping rather than rising.

HMM requires more assumptions than K-means. It relies on estimated transition probabilities that could be wrong, and once wrong, the model is biased toward staying in an incorrect regime rather than correcting quickly. K-means has no such bias, it just reacts to each day's data.

## Status / In Progress

Core analysis complete: feature engineering, rule-based comparison, energy pivot, HMM implementation.

Next: a regime-based trading strategy, backtested against historical data, combined with the Regime Instability Analysis project into a single dashboard.

## Related Work

This project builds directly on [Regime-Based Risk Instability in Financial Markets](https://github.com/pascalburki/regime-risk-instability), which defines regimes using manually-set volatility thresholds and identifies correlation, not volatility alone, as the primary driver of diversification failure under stress.
