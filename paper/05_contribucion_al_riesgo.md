## 5. Tercera capa del diagnóstico: ¿quién genera realmente el riesgo?

**Pregunta:** ¿Una cartera 60/40 por capital también es 60/40 por riesgo?

Con la estructura de dependencia ya caracterizada, el diagnóstico pasa de la correlación a la contribución al riesgo total del portafolio. Sobre los retornos logarítmicos diarios y los pesos objetivo constantes \(w\), se estima la covarianza muestral \(\Sigma\) y se define:

\[
\sigma_p = \sqrt{w^{\top}\Sigma w},
\quad
\mathrm{MRC}_i = \frac{(\Sigma w)_i}{\sigma_p},
\quad
\mathrm{RC}_i = w_i\,\mathrm{MRC}_i,
\quad
\mathrm{PRC}_i = \frac{\mathrm{RC}_i}{\sigma_p}.
\]

La identidad de Euler implica \(\sum_i \mathrm{RC}_i = \sigma_p\) y, por tanto, \(\sum_i \mathrm{PRC}_i = 1\).

**Resultados**

| Métrica | Valor |
|---------|-------|
| \(\sigma_p\) diaria | 0.0113 |
| \(\sigma_p\) anualizada (\(\times\sqrt{252}\)) | 17.99% |
| \(\sum \mathrm{PRC}_i\) | 1.0000 |

| Ticker | Peso | PRC |
|--------|------|-----|
| SPY | 8.57% | 7.12% |
| QQQ | 8.57% | 9.71% |
| SMH | 8.57% | 14.11% |
| NVDA | 8.57% | 19.12% |
| TSLA | 8.57% | 19.49% |
| MU | 8.57% | 18.18% |
| AAPL | 8.57% | 9.92% |
| BND | 13.33% | 1.09% |
| IEF | 13.33% | 0.39% |
| TLT | 13.33% | 0.87% |

| Clase | Capital | Riesgo (Σ PRC) |
|-------|---------|----------------|
| Renta variable | 60.0% | 97.65% |
| Renta fija | 40.0% | 2.35% |

**Figura 5.** Peso en cartera vs. contribución porcentual al riesgo.

**Figura 6.** Asignación de capital vs. asignación de riesgo.

Los resultados muestran una marcada disociación entre la asignación de capital y la distribución de las contribuciones al riesgo. Aunque el 60% del capital se encuentra asignado a renta variable, los instrumentos pertenecientes a esta clase concentran el 97.65% de la contribución total al riesgo del portafolio. En contraste, el bloque de renta fija, que representa el 40% del capital, concentra únicamente el 2.35% de la contribución al riesgo estimada mediante la descomposición de Euler.

La divergencia también es significativa a nivel de instrumento. TSLA, NVDA y MU reciben individualmente el mismo peso objetivo que el resto de las posiciones de renta variable —8.57%—, pero sus contribuciones porcentuales al riesgo alcanzan 19.49%, 19.12% y 18.18%, respectivamente. En comparación, SPY contribuye un 7.12% del riesgo total con idéntica asignación de capital.

Los resultados muestran que la equiponderación del capital no implica equiponderación del riesgo. En la muestra analizada, la clasificación 60/40 describe adecuadamente la estructura nominal de capital del portafolio, pero no su estructura de riesgo.
