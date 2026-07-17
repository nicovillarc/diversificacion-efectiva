## 7. Fifth diagnostic layer: how many common risk sources are there?

**Question:** How many components suffice to explain most of the portfolio’s joint variability?

As the final diagnostic layer, principal component analysis (PCA) is applied to the correlation matrix of daily log returns. PCA is used here solely as a descriptive tool for common sources of variation; it is not an optimization or portfolio-construction procedure.

**Results**

| Component | Explained variance | Cumulative |
|-----------|-------------------|------------|
| PC1 | 49.29% | 49.29% |
| PC2 | 27.11% | 76.40% |
| PC3 | 7.31% | 83.72% |
| PC4 | 6.06% | 89.78% |
| PC5 | 4.13% | 93.90% |

| Threshold | Components required |
|-----------|---------------------|
| ≥ 80% of joint variability | **3** |
| ≥ 90% of joint variability | **5** |

**Figure 8.** PCA — scree plot.  
**Figure 9.** Cumulative explained variance.  
**Figure 10.** Scaled loadings \(v_{ik}\sqrt{\lambda_k}\) (PC1–PC5).

Figure 10 reports scaled loadings, which equal the correlation between each standardized variable and the corresponding principal-component score. Pure eigenvectors are not displayed.

Any economic reading of the components must be derived from the observed loading pattern rather than imposed a priori. PC1 (49.3%) shows large same-sign correlations with equity instruments (e.g., QQQ 0.96, SMH 0.93, SPY 0.92), while associations with BND, IEF, and TLT are near zero or slightly negative. PC2 (27.1%) concentrates large same-sign correlations on BND, IEF, and TLT (≈ 0.94–0.96), with near-zero values on the equity block. That cross-block contrast is the empirical pattern that, cautiously, motivates associating PC1 with a common source dominated by equities and PC2 with a common source dominated by fixed income; they are not postulated here as exogenous observable factors. Later components explain smaller shares: PC3, for instance, combines a material positive correlation with TSLA (0.59) and a negative correlation with MU (−0.47), without a unique economic label.

Overall, joint variability in the ten-instrument universe concentrates in a small number of dimensions: three components meet the 80% threshold and five meet the 90% threshold. The nominal number of assets therefore exceeds the number of dominant common sources identified by PCA in the sample analyzed.
