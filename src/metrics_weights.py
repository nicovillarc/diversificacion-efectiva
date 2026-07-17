"""Métricas de concentración basadas únicamente en pesos objetivo."""

from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd


def weight_concentration(weights: Mapping[str, float] | pd.Series) -> dict[str, float]:
    """HHI y número efectivo de posiciones por capital.

    HHI = sum_i w_i^2
    N_eff,weights = 1 / HHI
    """
    w = pd.Series(weights, dtype=float)
    if not np.isclose(w.sum(), 1.0):
        raise ValueError(f"Weights must sum to 1; got {w.sum():.8f}")
    hhi = float((w ** 2).sum())
    n_eff = float(1.0 / hhi)
    return {
        "n_nominal": float(len(w)),
        "hhi": hhi,
        "n_eff_weights": n_eff,
        "sum_weights": float(w.sum()),
    }
