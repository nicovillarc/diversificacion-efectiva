## 3. Primera capa del diagnóstico: ¿cuántos activos tenemos?

**Pregunta:** ¿El número nominal de instrumentos describe adecuadamente la dispersión del capital?

El punto de partida del análisis es el número nominal de posiciones que integran la cartera:

\[
N = 10
\]

Sin embargo, el conteo de activos no permite identificar posibles concentraciones derivadas de la distribución de los pesos. Para evaluar esta dimensión se utiliza el índice de Herfindahl-Hirschman (HHI):

\[
\mathrm{HHI} = \sum_{i=1}^{N} w_i^2
\]

A partir de esta medida puede calcularse el número efectivo de posiciones por capital:

\[
N_{\mathrm{eff,weights}} = \frac{1}{\sum_{i=1}^{N} w_i^2} = \frac{1}{\mathrm{HHI}}
\]

Esta métrica expresa el número de posiciones equiponderadas que produciría un grado equivalente de concentración del capital.

**Resultados**

| Métrica | Valor |
|---------|-------|
| Número nominal de activos \(N\) | 10 |
| HHI | 0.1048 |
| \(N_{\mathrm{eff,weights}}\) | 9.55 |

**Figura 2.** Activos nominales vs. posiciones efectivas por capital.

Los resultados muestran que, desde la perspectiva de la asignación de capital, el portafolio presenta una elevada dispersión. Las diez posiciones nominales equivalen a 9.55 posiciones equiponderadas efectivas, una diferencia reducida explicada por el mayor peso individual de los tres instrumentos de renta fija (13.33%) frente a cada posición de renta variable (8.57%).

Por lo tanto, no se observa una concentración significativa del capital derivada de los pesos objetivo.

Sin embargo, esta primera aproximación no incorpora la dependencia entre los retornos ni la contribución de cada activo al riesgo total. La concentración del capital constituye únicamente la primera capa del diagnóstico.
