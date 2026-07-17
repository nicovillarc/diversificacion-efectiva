# Beyond the Number of Assets: Measuring True Portfolio Diversification

**Subtitle.** A quantitative approach to assessing risk concentration in an investment portfolio

## 1. Introduction

**Conceptual question:** Does holding more assets necessarily mean being more diversified?

Diversification is central to portfolio management. In practice, however, it is often approximated informally by the number of instruments in a portfolio. That nominal count is intuitive, but it readily confuses three distinct planes: the quantity of assets, the distribution of capital, and the structure of risk.

Holding different instruments does not guarantee independent exposures. A broad market index, a sector ETF, and an individual stock can share common sources of variation; their returns may move together even when their tickers differ. Likewise, a balanced capital allocation—for example, a 60/40 split between equities and fixed income—does not, by itself, imply a balanced distribution of risk contributions. Overlapping exposures between ETFs and individual securities, and the gap between capital allocation and risk allocation, motivate a diagnosis that goes beyond counting positions.

**Research question.** To what extent does the number of assets in a portfolio reflect its effective degree of diversification?

**Hypothesis.** The nominal number of assets is, by itself, an insufficient measure of diversification when instruments exhibit material dependence and common risk sources. The hypothesis is evaluated empirically; it is not assumed before observing the results.

**Objective.** The objective of this study is exclusively diagnostic: to analyze the actual risk structure of a portfolio before attempting to optimize it. The paper does not seek an optimal allocation or a comparison of investment methodologies. In particular, it is not a study of Markowitz, Risk Parity, Hierarchical Risk Parity (HRP), or PCA as an optimization tool.

The analysis proceeds in successive layers on the same 60/40 portfolio over the window 2016-01-01 to 2026-06-30:

1. nominal number of assets and weight concentration;
2. dependence structure among returns;
3. each instrument’s contribution to total risk;
4. effective number of positions by capital and by risk;
5. identification of common sources of variation via PCA.

The narrative logic is constant: one question, one metric, one figure, one result, and one interpretation. Conclusions are drawn from the empirical evidence generated at each layer.
