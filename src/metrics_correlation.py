"""Métricas de dependencia basadas en la matriz de correlación de retornos log."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def mean_off_diagonal(corr: pd.DataFrame) -> float:
    values = corr.values
    mask = ~np.eye(len(corr), dtype=bool)
    return float(values[mask].mean())


def pairwise_correlations(corr: pd.DataFrame) -> pd.DataFrame:
    """Pares únicos (triángulo superior), sin diagonal."""
    rows = []
    cols = list(corr.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            rows.append({"asset_i": a, "asset_j": b, "correlation": float(corr.loc[a, b])})
    return pd.DataFrame(rows)


def top_bottom_pairs(corr: pd.DataFrame, n: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairs = pairwise_correlations(corr)
    highest = pairs.sort_values("correlation", ascending=False).head(n).reset_index(drop=True)
    lowest = pairs.sort_values("correlation", ascending=True).head(n).reset_index(drop=True)
    return highest, lowest


def correlation_summary(
    corr: pd.DataFrame,
    equity_tickers: Iterable[str],
    fixed_income_tickers: Iterable[str],
    threshold: float,
) -> dict[str, float | int]:
    equity = list(equity_tickers)
    fixed = list(fixed_income_tickers)
    eq = corr.loc[equity, equity]
    fi = corr.loc[fixed, fixed]
    cross = corr.loc[equity, fixed]

    triu = corr.values[np.triu_indices(len(corr), k=1)]
    n_edges = int((np.abs(triu) >= threshold).sum())

    return {
        "mean_correlation": mean_off_diagonal(corr),
        "mean_correlation_equity": mean_off_diagonal(eq),
        "mean_correlation_fixed_income": mean_off_diagonal(fi),
        "mean_correlation_cross": float(cross.values.mean()),
        "min_pairwise": float(triu.min()),
        "max_pairwise": float(triu.max()),
        "n_edges_above_threshold": n_edges,
        "threshold": float(threshold),
        "n_assets": len(corr),
    }


def correlation_edges(
    corr: pd.DataFrame,
    threshold: float,
) -> pd.DataFrame:
    pairs = pairwise_correlations(corr)
    edges = pairs.loc[pairs["correlation"].abs() >= threshold].copy()
    return edges.sort_values(
        "correlation", key=lambda s: s.abs(), ascending=False
    ).reset_index(drop=True)
