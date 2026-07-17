## 3. First diagnostic layer: how many assets do we have?

**Question:** Does the nominal number of instruments adequately describe the dispersion of capital?

The analysis begins with the nominal number of positions in the portfolio:

\[
N = 10
\]

However, counting assets does not reveal possible concentrations arising from the distribution of weights. To assess this dimension, the Herfindahl-Hirschman Index (HHI) is used:

\[
\mathrm{HHI} = \sum_{i=1}^{N} w_i^2
\]

From this measure, the effective number of positions by capital can be computed:

\[
N_{\mathrm{eff,weights}} = \frac{1}{\sum_{i=1}^{N} w_i^2} = \frac{1}{\mathrm{HHI}}
\]

This metric expresses the number of equal-weighted positions that would produce an equivalent degree of capital concentration.

**Results**

| Metric | Value |
|--------|-------|
| Nominal number of assets \(N\) | 10 |
| HHI | 0.1048 |
| \(N_{\mathrm{eff,weights}}\) | 9.55 |

**Figure 2.** Nominal assets vs. effective positions by capital.

The results show that, from a capital-allocation perspective, the portfolio exhibits high dispersion. The ten nominal positions are equivalent to 9.55 equal-weighted effective positions—a small gap explained by the larger individual weight of each of the three fixed-income instruments (13.33%) relative to each equity position (8.57%).

Therefore, no material capital concentration is observed from the target weights alone.

This first approximation, however, does not incorporate dependence among returns or each asset’s contribution to total risk. Capital concentration is only the first layer of the diagnosis.
