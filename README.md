# Más allá del número de activos

Diagnóstico cuantitativo de diversificación efectiva sobre una cartera 60/40.

**Idea central:** la diversificación no se mide contando activos; se mide evaluando cuántas fuentes de riesgo independientes tiene realmente un portafolio.

---

## Entregables

| Documento | Archivo |
|-----------|---------|
| Paper académico (autor: Villar Capital) | [`Más allá del número de activos — Villar Capital.pdf`](./Más%20allá%20del%20número%20de%20activos%20—%20Villar%20Capital.pdf) |
| Informe institucional (Portfolio Diagnostics #001) | [`Portfolio Research Report — Diversificación efectiva.pdf`](./Portfolio%20Research%20Report%20—%20Diversificación%20efectiva.pdf) |
| Carrusel Instagram | [`instagram/carousel/`](./instagram/carousel/) |

---

## Caso de estudio

- Cartera diagnóstico **60/40** con **10 instrumentos**
- Pesos objetivo constantes (sin backtest ni rebalanceo)
- Ventana: **2016-01-01 → 2026-06-30**
- Retornos logarítmicos diarios (precios ajustados, Yahoo Finance)

**Equity (60%):** SPY, QQQ, SMH, NVDA, TSLA, MU, AAPL  
**Fixed income (40%):** BND, IEF, TLT

---

## Resultados en un vistazo

```
10 activos nominales
 → 9.55 posiciones efectivas por capital
 → 6.58 posiciones efectivas por riesgo
 → 3 fuentes principales (≥80% de la variación conjunta)
```

- Renta variable aporta **97.65%** del riesgo total
- Renta fija aporta **2.35%** del riesgo total (con 40% del capital)

---

## Estructura del repositorio

```
src/           Código (descarga, métricas, figuras, carrusel)
data/raw/      Precios ajustados
data/processed/ Matrices, PRC, PCA, auditorías
figures/       Figuras del paper e informe (ES/EN)
paper/         Paper académico (Markdown + LaTeX + PDF)
report/        Informe institucional (LaTeX + PDF)
instagram/     Carrusel 1080×1080
```

---

## Reproducir

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Descargar / actualizar datos
python3 src/download_data.py

# Métricas y figuras (ejemplos)
python3 src/metrics_weights.py
python3 src/metrics_correlation.py
python3 src/metrics_risk.py
python3 src/metrics_effective_positions.py
python3 src/metrics_pca.py
python3 src/fig01_portfolio_allocation.py
# … resto de fig0x_*.py

# Carrusel Instagram
python3 src/instagram_carousel.py
```

### Compilar PDFs (LaTeX)

Requiere un motor TeX (p. ej. [Tectonic](https://tectonic-typesetting.github.io/)):

```bash
cd paper
tectonic -X compile diversificacion_efectiva_es_villar_capital.tex

cd ../report
tectonic -X compile portfolio_research_report_es.tex
```

---

## Nota metodológica

El estudio es **exclusivamente diagnóstico**: no optimiza la cartera ni prescribe Markowitz, Risk Parity, HRP ni Black-Litterman.

---

## Autor

**Villar Capital**  
Julio 2026
