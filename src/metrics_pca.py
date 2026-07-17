"""PCA diagnóstico sobre la matriz de correlación de retornos log."""

from __future__ import annotations

import numpy as np
import pandas as pd


def pca_from_correlation(returns: pd.DataFrame) -> dict:
    """Eigen-descomposición de la matriz de correlación (retornos estandarizados).

    Equivalente a PCA sobre retornos con media 0 y varianza 1.
    No es un modelo de inversión: solo diagnóstico de fuentes comunes.

    Definiciones:
      - eigenvectors: columnas de V (ortonormales)
      - scaled_loadings: v_ik * sqrt(λ_k)
        ≡ correlación entre la variable estandarizada i y el score del PCk
    """
    tickers = list(returns.columns)
    corr = returns.corr().loc[tickers, tickers]
    evals, evecs = np.linalg.eigh(corr.values)

    # Orden descendente de varianza explicada
    order = np.argsort(evals)[::-1]
    evals = evals[order]
    evecs = evecs[:, order]

    # Convención de signo: entrada de mayor |valor| positiva
    for j in range(evecs.shape[1]):
        k = int(np.argmax(np.abs(evecs[:, j])))
        if evecs[k, j] < 0:
            evecs[:, j] *= -1

    total = float(evals.sum())
    explained = evals / total
    cumulative = np.cumsum(explained)

    n_comp = len(evals)
    labels = [f"PC{i+1}" for i in range(n_comp)]
    eigenvectors = pd.DataFrame(evecs, index=tickers, columns=labels)
    scaled_loadings = pd.DataFrame(
        evecs * np.sqrt(evals), index=tickers, columns=labels
    )

    def n_for_threshold(thr: float) -> int:
        return int(np.searchsorted(cumulative, thr) + 1)

    return {
        "tickers": tickers,
        "correlation": corr,
        "eigenvalues": pd.Series(evals, index=labels, name="eigenvalue"),
        "explained_variance_ratio": pd.Series(
            explained, index=labels, name="explained_variance_ratio"
        ),
        "cumulative_explained_variance": pd.Series(
            cumulative, index=labels, name="cumulative_explained_variance"
        ),
        "eigenvectors": eigenvectors,
        "scaled_loadings": scaled_loadings,
        # Alias de compatibilidad: "loadings" = scaled (representación del paper)
        "loadings": scaled_loadings,
        "n_components_80": n_for_threshold(0.80),
        "n_components_90": n_for_threshold(0.90),
        "n_assets": n_comp,
    }


def loadings_subset(loadings: pd.DataFrame, n: int) -> pd.DataFrame:
    cols = list(loadings.columns[:n])
    return loadings[cols]
