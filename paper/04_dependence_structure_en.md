## 4. Second diagnostic layer: how do the assets move?

**Question:** Do ten instruments represent ten independent behaviors?

After examining capital dispersion, the diagnosis turns to the dependence structure among returns. Pearson correlations are estimated on daily log returns over the fixed window 2016-01-01 to 2026-06-30 (\(T = 2{,}636\) observations).

**Aggregate results**

| Metric | Value |
|--------|-------|
| Mean correlation (off-diagonal pairs) | 0.34 |
| Mean within-equity correlation | 0.63 |
| Mean within–fixed income correlation | 0.86 |
| Mean cross-class correlation | −0.03 |
| Min / max pairwise correlation | −0.16 / 0.93 |
| Edges with \(\lvert\rho\rvert \ge 0.60\) | 15 |

**Figure 3.** Return correlation matrix.

The matrix reveals two blocks of elevated dependence. Within equity, intra-class correlations are generally high: SPY–QQQ reaches 0.93 and QQQ–SMH 0.88, with strong links also among SMH, NVDA, MU, and AAPL. Within fixed income, BND, IEF, and TLT form an even tighter block (correlations between 0.80 and 0.91). Cross-class correlations, by contrast, cluster near zero, with moderately negative values between Treasuries (IEF, TLT) and several equities.

**Figure 4.** Correlation network (\(\lvert\rho\rvert \ge 0.60\)).

The graph visually confirms two asset-class clusters and the absence of cross-class edges above the threshold. TSLA appears as an isolated node: its correlations with the rest of the universe remain below 0.60 (maximum 0.57 with QQQ).

Overall, the ten instruments do not behave as ten independent sources of variation. Dependence is high *within* each asset class and low *across* classes, pointing to overlapping exposures—especially within the technology/semiconductor equity block and within fixed income—while preserving the diversifying potential of the 60/40 split. The next layer quantifies that redundancy in risk terms.
