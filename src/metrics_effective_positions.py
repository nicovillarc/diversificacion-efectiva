"""Números efectivos de posiciones: por capital y por riesgo."""

from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd

from metrics_weights import weight_concentration


def risk_concentration(prc: Mapping[str, float] | pd.Series) -> dict[str, float]:
    """HHI y N_eff basados en la contribución porcentual al riesgo.

    p_i = PRC_i,  sum p_i = 1
    HHI_risk = sum p_i^2
    N_eff,risk = 1 / HHI_risk
    """
    p = pd.Series(prc, dtype=float)
    if not np.isclose(p.sum(), 1.0, rtol=1e-8, atol=1e-10):
        raise ValueError(f"PRC must sum to 1; got {p.sum():.12f}")
    hhi = float((p ** 2).sum())
    n_eff = float(1.0 / hhi)
    return {
        "hhi_risk": hhi,
        "n_eff_risk": n_eff,
        "sum_prc": float(p.sum()),
        "n_assets": float(len(p)),
    }


def effective_positions_summary(
    weights: Mapping[str, float] | pd.Series,
    prc: Mapping[str, float] | pd.Series,
) -> dict[str, float]:
    w_metrics = weight_concentration(weights)
    r_metrics = risk_concentration(prc)
    return {
        "n_nominal": w_metrics["n_nominal"],
        "hhi_weights": w_metrics["hhi"],
        "n_eff_weights": w_metrics["n_eff_weights"],
        "hhi_risk": r_metrics["hhi_risk"],
        "n_eff_risk": r_metrics["n_eff_risk"],
        "sum_weights": w_metrics["sum_weights"],
        "sum_prc": r_metrics["sum_prc"],
    }
