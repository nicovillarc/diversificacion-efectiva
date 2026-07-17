## 6. Fourth diagnostic layer: how many effective positions do we have?

**Question:** How much does the number of positions shrink when moving from the nominal count to capital concentration and, finally, to risk concentration?

Three metrics are compared:

\[
N = 10,
\qquad
N_{\mathrm{eff,weights}} = \frac{1}{\sum_{i=1}^{N} w_i^2},
\qquad
N_{\mathrm{eff,risk}} = \frac{1}{\sum_{i=1}^{N} p_i^2},
\quad p_i = \mathrm{PRC}_i.
\]

\(N_{\mathrm{eff,weights}}\) expresses the number of equal-weighted positions that would produce an equivalent degree of capital concentration. \(N_{\mathrm{eff,risk}}\) applies the same principle to the distribution of percentage risk contributions.

**Results**

| Metric | Value |
|--------|-------|
| Nominal number of assets \(N\) | 10 |
| \(N_{\mathrm{eff,weights}}\) | 9.55 |
| \(N_{\mathrm{eff,risk}}\) | 6.58 |
| HHI (weights) | 0.1048 |
| HHI (risk) | 0.1521 |

**Figure 7.** Nominal assets vs. effective positions by capital and by risk.

From a capital perspective, the ten nominal positions are equivalent to 9.55 equal-weighted positions: target-weight dispersion is high and barely departs from the nominal count. When the concentration of percentage risk contributions is assessed, the effective number falls to 6.58. The contraction reflects the concentration of risk contributions in a subset of equity instruments—particularly TSLA, NVDA, and MU—documented in the previous layer.

In short, the portfolio exhibits high dispersion when analyzed solely through capital allocation; once the distribution of risk contributions is incorporated, the effective number of positions declines materially relative to the nominal count.
