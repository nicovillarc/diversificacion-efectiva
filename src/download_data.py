"""Descarga precios ajustados y construye la muestra común de retornos log.

Usa la ventana fija [START_DATE, END_DATE] (END_DATE inclusiva) para
garantizar reproducibilidad. Los pesos objetivo constantes se exportan
tal cual están definidos en config; no se simula drift ni rebalanceo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import END_DATE, START_DATE, TICKERS, WEIGHTS  # noqa: E402

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


def _yf_end_exclusive(end_inclusive: str) -> str:
    """yfinance trata `end` como exclusivo; sumamos un día calendario."""
    return (pd.Timestamp(end_inclusive) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")


def download_prices() -> pd.DataFrame:
    raw = yf.download(
        TICKERS,
        start=START_DATE,
        end=_yf_end_exclusive(END_DATE),
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    # Con auto_adjust=True, Close ya está ajustado
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"].copy()
    else:
        prices = raw[["Close"]].copy()
        prices.columns = TICKERS[:1]

    prices = prices.reindex(columns=TICKERS).sort_index()
    # Recorte explícito a la ventana inclusiva fija
    start = pd.Timestamp(START_DATE)
    end = pd.Timestamp(END_DATE)
    return prices.loc[(prices.index >= start) & (prices.index <= end)]


def build_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    clean = prices.dropna(how="any")
    returns = np.log(clean / clean.shift(1)).dropna(how="any")
    returns.index.name = "date"
    return returns


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    prices = download_prices()
    prices.to_csv(RAW_DIR / "prices_adj_close.csv")

    prices_common = prices.dropna(how="any")
    prices_common.to_csv(PROCESSED_DIR / "prices_common.csv")

    returns = build_log_returns(prices)
    returns.to_csv(PROCESSED_DIR / "log_returns.csv")

    # Pesos objetivo constantes (diagnóstico estático); no drift / no rebalanceo
    weights = pd.Series(WEIGHTS, name="weight")
    weights.to_csv(PROCESSED_DIR / "weights.csv", header=True)

    missing_by_ticker = prices.isna().sum()
    print("=== Verificación de muestra ===")
    print(f"Ventana fija (inclusiva): {START_DATE} → {END_DATE}")
    print(f"Tickers: {list(prices.columns)}")
    print(f"Primera fecha con dato: {prices.first_valid_index().date()}")
    print(f"Última fecha con dato: {prices.last_valid_index().date()}")
    print(f"Días raw: {len(prices)}")
    print(f"Días comunes (sin NaN): {len(prices_common)}")
    print(f"Observaciones retornos log: {len(returns)}")
    print(f"Rango retornos: {returns.index.min().date()} → {returns.index.max().date()}")
    print(f"Suma de pesos objetivo: {weights.sum():.6f}")
    print("\nNaN por ticker (precios raw):")
    print(missing_by_ticker.to_string())
    print("\nPesos objetivo constantes:")
    print(weights.map(lambda w: f"{w:.4%}").to_string())
    print("\nArchivos guardados en data/raw y data/processed.")


if __name__ == "__main__":
    main()
