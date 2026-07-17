## 5. Third diagnostic layer: who actually generates the risk?

**Question:** Is a 60/40 portfolio by capital also 60/40 by risk?

With the dependence structure characterized, the diagnosis moves from correlation to each position’s contribution to total portfolio risk. Using daily log returns and constant target weights \(w\), the sample covariance \(\Sigma\) is estimated and:

\[
\sigma_p = \sqrt{w^{\top}\Sigma w},
\quad
\mathrm{MRC}_i = \frac{(\Sigma w)_i}{\sigma_p},
\quad
\mathrm{RC}_i = w_i\,\mathrm{MRC}_i,
\quad
\mathrm{PRC}_i = \frac{\mathrm{RC}_i}{\sigma_p}.
\]

Euler’s identity implies \(\sum_i \mathrm{RC}_i = \sigma_p\) and therefore \(\sum_i \mathrm{PRC}_i = 1\).

**Results**

| Metric | Value |
|--------|-------|
| Daily \(\sigma_p\) | 0.0113 |
| Annualized \(\sigma_p\) (\(\times\sqrt{252}\)) | 17.99% |
| \(\sum \mathrm{PRC}_i\) | 1.0000 |

| Ticker | Weight | PRC |
|--------|--------|-----|
| SPY | 8.57% | 7.12% |
| QQQ | 8.57% | 9.71% |
| SMH | 8.57% | 14.11% |
| NVDA | 8.57% | 19.12% |
| TSLA | 8.57% | 19.49% |
| MU | 8.57% | 18.18% |
| AAPL | 8.57% | 9.92% |
| BND | 13.33% | 1.09% |
| IEF | 13.33% | 0.39% |
| TLT | 13.33% | 0.87% |

| Asset class | Capital | Risk (Σ PRC) |
|-------------|---------|--------------|
| Equity | 60.0% | 97.65% |
| Fixed income | 40.0% | 2.35% |

**Figure 5.** Portfolio weight vs. percentage risk contribution.

**Figure 6.** Capital allocation vs. risk allocation.

The results show a marked dissociation between capital allocation and the distribution of risk contributions. Although 60% of capital is allocated to equities, instruments in this asset class account for 97.65% of the portfolio’s total risk contribution. By contrast, the fixed-income block, which represents 40% of capital, accounts for only 2.35% of the risk contribution estimated via Euler’s decomposition.

The divergence is also material at the instrument level. TSLA, NVDA, and MU each receive the same target weight as the remaining equity positions—8.57%—yet their percentage risk contributions reach 19.49%, 19.12%, and 18.18%, respectively. By comparison, SPY contributes 7.12% of total risk with an identical capital allocation.

The results show that equal weighting in capital does not imply equal weighting in risk. In the sample analyzed, the 60/40 classification adequately describes the portfolio’s nominal capital structure, but not its risk structure.
