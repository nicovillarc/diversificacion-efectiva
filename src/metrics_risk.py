"""Contribuciones al riesgo del portafolio (diagnóstico estático)."""

from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd


def portfolio_risk_contributions(
    returns: pd.DataFrame,
    weights: Mapping[str, float] | pd.Series,
    annualization_factor: int = 252,
) -> dict:
    """Calcula σ_p, MRC, RC y PRC con pesos objetivo constantes.

    Definiciones (escala diaria de Σ):
        σ_p = sqrt(w' Σ w)
        MRC_i = (Σ w)_i / σ_p
        RC_i = w_i * MRC_i
        PRC_i = RC_i / σ_p

    Identidad: sum_i RC_i = σ_p  ⇒  sum_i PRC_i = 1
    """
    tickers = list(returns.columns)
    w = pd.Series(weights, dtype=float).reindex(tickers)
    if w.isna().any():
        missing = w[w.isna()].index.tolist()
        raise ValueError(f"Missing weights for: {missing}")
    if not np.isclose(w.sum(), 1.0):
        raise ValueError(f"Weights must sum to 1; got {w.sum():.8f}")

    cov = returns.cov().loc[tickers, tickers]
    sigma = cov.values
    w_vec = w.values.astype(float)

    port_var = float(w_vec @ sigma @ w_vec)
    if port_var <= 0:
        raise ValueError("Portfolio variance must be positive")
    sigma_p = float(np.sqrt(port_var))

    sigma_w = sigma @ w_vec
    mrc = sigma_w / sigma_p
    rc = w_vec * mrc
    prc = rc / sigma_p

    detail = pd.DataFrame(
        {
            "weight": w_vec,
            "mrc": mrc,
            "rc": rc,
            "prc": prc,
        },
        index=tickers,
    )
    detail.index.name = "ticker"

    # Verificación de identidad Euler
    sum_rc = float(detail["rc"].sum())
    sum_prc = float(detail["prc"].sum())

    return {
        "tickers": tickers,
        "covariance": cov,
        "sigma_p_daily": sigma_p,
        "sigma_p_annual": sigma_p * np.sqrt(annualization_factor),
        "detail": detail,
        "sum_rc": sum_rc,
        "sum_prc": sum_prc,
        "identity_ok": bool(
            np.isclose(sum_rc, sigma_p, rtol=1e-8, atol=1e-12)
            and np.isclose(sum_prc, 1.0, rtol=1e-8, atol=1e-12)
        ),
    }


def class_aggregates(
    detail: pd.DataFrame,
    asset_class: Mapping[str, str],
) -> pd.DataFrame:
    df = detail.copy()
    df["asset_class"] = [asset_class[t] for t in df.index]
    agg = (
        df.groupby("asset_class", sort=False)[["weight", "prc", "rc"]]
        .sum()
        .rename(columns={"weight": "capital_weight", "prc": "risk_share"})
    )
    return agg
