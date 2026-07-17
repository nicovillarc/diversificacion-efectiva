"""Convenciones metodológicas del estudio.

Estudio exclusivamente de portfolio diagnostics.
No incorpora optimización (Markowitz, HRP, Risk Parity, Black-Litterman, CVaR).
No realiza backtest, buy-and-hold ni modelado del drift de pesos.
Las conclusiones deben derivarse de resultados empíricos; no hardcodearlas.
"""

from __future__ import annotations

# Ventana fija (reproducible). END_DATE es inclusiva.
START_DATE = "2016-01-01"
END_DATE = "2026-06-30"

# Cartera 60/40: pesos objetivo constantes para diagnóstico estático.
# Equity 60% equiponderado; fixed income 40% equiponderado.
# No implica rebalanceo periódico ni simulación dinámica de pesos.
EQUITY_TICKERS = ["SPY", "QQQ", "SMH", "NVDA", "TSLA", "MU", "AAPL"]
FIXED_INCOME_TICKERS = ["BND", "IEF", "TLT"]
TICKERS = EQUITY_TICKERS + FIXED_INCOME_TICKERS

EQUITY_WEIGHT = 0.60
FIXED_INCOME_WEIGHT = 0.40

WEIGHTS = {
    **{t: EQUITY_WEIGHT / len(EQUITY_TICKERS) for t in EQUITY_TICKERS},
    **{t: FIXED_INCOME_WEIGHT / len(FIXED_INCOME_TICKERS) for t in FIXED_INCOME_TICKERS},
}

ASSET_CLASS = {
    **{t: "equity" for t in EQUITY_TICKERS},
    **{t: "fixed_income" for t in FIXED_INCOME_TICKERS},
}

# Datos: retornos log diarios, usados de forma consistente en
# covarianza, correlaciones, contribución al riesgo y PCA.
DATA_SOURCE = "Yahoo Finance"
PRICE_FIELD = "Adj Close"
FREQUENCY = "daily"
RETURN_TYPE = "log"  # r_t = ln(P_t / P_{t-1})
ANNUALIZATION_FACTOR = 252

# Secuencia conceptual del análisis (diagnóstico progresivo):
# 1) número nominal de activos
# 2) concentración de pesos
# 3) estructura de dependencia
# 4) contribución al riesgo
# 5) N_eff por capital
# 6) N_eff por riesgo
# 7) fuentes comunes de riesgo (PCA)
ANALYSIS_SEQUENCE = (
    "nominal_assets",
    "weight_concentration",
    "dependence_structure",
    "risk_contribution",
    "effective_positions_capital",
    "effective_positions_risk",
    "common_risk_sources_pca",
)

# Visualización (ajustable después; no implica conclusión)
CORR_NETWORK_THRESHOLD = 0.60
