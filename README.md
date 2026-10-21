# K-Means Market Regime Detection

## Summary

This project tests whether K-means clustering, a type of unsupervised machine learning, can find market regimes directly from the data without me setting any thresholds by hand. It follows my Regime Instability Analysis project, where I defined regimes with volatility percentiles that I chose myself.

K-means gets the raw features (returns, volatility and the correlation between two assets) and finds its own groups. I then compare those groups with a simple rule-based method. Later I tested it on energy market data and added a Hidden Markov Model, because K-means has a real limitation: it has no memory of time.

**A note on the process:** I had to fix two real bugs in this project. First, the features weren't scaled, so correlation dominated the clustering. Second, I had hardcoded which cluster meant which regime, and that mapping broke once the clusters changed. Because of this, I changed or took back some early findings. Everything below is the corrected version, and I reran every script to check it. The full history of what I first found, what turned out to be wrong and why is in `progress_log.md`.

## Assets and data

- **SPY, QQQ:** daily data, 2018-2023 (1,489 trading days after cleaning), as the equity baseline.
- **NG=F (natural gas futures):** daily data, 2018-2023, for the energy test.
- **GLD:** daily data, 2018-2023, to compare correlation across different assets.

## Method

**Features:** daily log returns, 20-day rolling volatility and, where noted, the 20-day rolling correlation between two assets. I standardize all features (StandardScaler) before clustering, so no feature dominates just because its numbers are bigger.

**Clustering:** K-means with K=3, checked with the elbow method (K=2 to K=5).

**Comparison:** a rule-based method using 20-day volatility percentiles (bottom 30% = low, middle 40% = medium, top 30% = high), compared with the K-means clusters in a crosstab. I decide which cluster means which regime from each run's actual statistics (ranked by average volatility or average return). K-means cluster numbers are arbitrary, so they can't be hardcoded.

**HMM:** a Gaussian Hidden Markov Model with 3 hidden states, fit on the same standardized features and compared directly with K-means.

## Key findings

**Baseline (returns and volatility, SPY):** K-means makes clusters of 1024, 29 and 436 days. The 29-day cluster is a clear stress regime (average return -0.007, average volatility 0.049), well separated from the calm cluster (1024 days, return near zero) and the moderate positive one (436 days).

**Elbow method:** the inertia goes from 2121 (K=2) to 1584 (K=3) to 1276 (K=4) to 857 (K=5). The biggest single improvement is from K=2 to K=3, which supports using K=3.

**Adding correlation as a third feature (SPY/QQQ):** clusters of 371, 30 and 1088 days, with the same kind of small, high-volatility cluster (average volatility 0.049) as the baseline.

**Window length:** with a 10-day window there is no small, sharp outlier cluster at all (the biggest high-volatility group is 307 days, 20% of the data). It is noisier and less separated than the 20-day window (30-day outlier) or the 60-day window (64-day outlier). Shorter windows weaken the signal.

**Comparing assets (SPY/GLD vs. SPY/QQQ):** once the features are scaled, both pairs give almost the same small outlier cluster (30-32 days, volatility about 0.048-0.049). I found no evidence that a more correlated second asset changes how well the regimes separate.

**Energy (NG=F):** clusters of 799, 317 and 374 days. Cluster 1 (average return -0.050, average volatility 0.055) is the stress regime. Cluster 2 (average return 0.044, average volatility 0.051) is an extreme positive regime. Both are concentrated in 2022 (101 and 114 days) and 2020 (61 and 81 days), which fits the Ukraine energy crisis and COVID.

**Energy vs. the rule-based method:** when I group the days where the two methods disagree into periods, instead of looking at single dates, a pattern shows up. There are 147 days in 20 periods where K-means said "extreme positive" and the rule-based method said "medium", and 217 days in 10 periods for the negative and high case. Several periods match known events: Nov 2018 to Feb 2019, the 2020 COVID crash, the run-up to the Ukraine invasion (Oct 2021 to Mar 2022), and a long stretch from Oct 2022 to May 2023 that I can only partly explain.

**Adding the HMM:** hidden states of 605, 20 and 865 days on NG=F, with only 16 regime switches against K-means's 536 on the same data. The HMM switches far less because it models how regimes last over time, while K-means treats every day on its own.

## Limitations

- The window length changes how well the clusters separate. Shorter windows are noisier.
- I found no evidence that the correlation between assets changes how well the regimes separate (tested on SPY/QQQ and SPY/GLD).
- The HMM needs more assumptions than K-means (estimating the transition probabilities, sensitivity to the starting values).
- Both bugs from the note above gave results that looked believable, with no errors or crashes. That makes them easy to miss, because nothing looks broken. Any future version should treat cluster numbers as arbitrary in every run and check the feature scaling before drawing conclusions from the clusters.

## Status

The core analysis is complete. All known bugs are fixed and checked by rerunning the scripts. Nothing is open.

Next: it was combined into the Regime Strategy Dashboard (separate repo).

## Related work

This project builds on Regime-Based Risk Instability in Financial Markets, which defines regimes with volatility thresholds set by hand and finds that correlation, not volatility alone, is the main reason diversification fails under stress.

## How I worked

I chose the project, the questions and what to test, ran the code and checked the results. I used an AI tutor (Claude) to help me learn the methods and to debug the code.
