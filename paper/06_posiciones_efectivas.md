## 6. Cuarta capa del diagnóstico: ¿cuántas posiciones efectivas tenemos?

**Pregunta:** ¿Cuánto se reduce el número de posiciones al pasar del conteo nominal a la concentración del capital y, finalmente, a la del riesgo?

Se comparan tres métricas:

\[
N = 10,
\qquad
N_{\mathrm{eff,weights}} = \frac{1}{\sum_{i=1}^{N} w_i^2},
\qquad
N_{\mathrm{eff,risk}} = \frac{1}{\sum_{i=1}^{N} p_i^2},
\quad p_i = \mathrm{PRC}_i.
\]

\(N_{\mathrm{eff,weights}}\) expresa el número de posiciones equiponderadas equivalentes en términos de concentración de capital. \(N_{\mathrm{eff,risk}}\) aplica el mismo principio a la distribución de las contribuciones porcentuales al riesgo.

**Resultados**

| Métrica | Valor |
|---------|-------|
| Número nominal de activos \(N\) | 10 |
| \(N_{\mathrm{eff,weights}}\) | 9.55 |
| \(N_{\mathrm{eff,risk}}\) | 6.58 |
| HHI (pesos) | 0.1048 |
| HHI (riesgo) | 0.1521 |

**Figura 7.** Activos nominales vs. posiciones efectivas por capital y por riesgo.

Desde la perspectiva del capital, las diez posiciones nominales equivalen a 9.55 posiciones equiponderadas: la dispersión de los pesos objetivo es elevada y apenas se distancia del conteo nominal. Al evaluar la concentración de las contribuciones porcentuales al riesgo, el número efectivo desciende a 6.58. La contracción refleja la concentración de las contribuciones al riesgo en un subconjunto de instrumentos de renta variable —en particular TSLA, NVDA y MU—, documentada en la capa anterior.

En síntesis, el portafolio presenta una elevada dispersión cuando se analiza exclusivamente la asignación de capital; una vez incorporada la distribución de las contribuciones al riesgo, el número efectivo de posiciones se reduce de forma material respecto del conteo nominal.
