## 7. Quinta capa del diagnóstico: ¿cuántas fuentes comunes de riesgo existen?

**Pregunta:** ¿Cuántos componentes bastan para explicar la mayor parte de la variabilidad conjunta del portafolio?

Como última capa del diagnóstico se aplica un análisis de componentes principales (PCA) sobre la matriz de correlación de los retornos logarítmicos diarios. El PCA se utiliza aquí exclusivamente como herramienta descriptiva de fuentes comunes de variación; no constituye un procedimiento de optimización ni de construcción de cartera.

**Resultados**

| Componente | Varianza explicada | Acumulada |
|------------|-------------------|-----------|
| PC1 | 49.29% | 49.29% |
| PC2 | 27.11% | 76.40% |
| PC3 | 7.31% | 83.72% |
| PC4 | 6.06% | 89.78% |
| PC5 | 4.13% | 93.90% |

| Umbral | Componentes necesarios |
|--------|------------------------|
| ≥ 80% de la variabilidad conjunta | **3** |
| ≥ 90% de la variabilidad conjunta | **5** |

**Figura 8.** PCA — gráfico de sedimentación (scree).  
**Figura 9.** Varianza explicada acumulada.  
**Figura 10.** Loadings escalados \(v_{ik}\sqrt{\lambda_k}\) (PC1–PC5).

La Figura 10 reporta loadings escalados, equivalentes a la correlación entre cada variable estandarizada y el score del componente correspondiente. No se representan los eigenvectors puros.

La lectura económica de los componentes, si se formula, debe derivarse del patrón observado en esos loadings y no imponerse a priori. PC1 (49.3%) muestra correlaciones elevadas y del mismo signo con los instrumentos de renta variable (p. ej., QQQ 0.96, SMH 0.93, SPY 0.92), mientras que las asociaciones con BND, IEF y TLT son cercanas a cero o ligeramente negativas. PC2 (27.1%) concentra correlaciones altas y del mismo signo con BND, IEF y TLT (≈ 0.94–0.96), con valores próximos a cero en el bloque equity. Ese contraste entre bloques es el patrón empírico que motiva, con cautela, asociar PC1 a una fuente común dominada por renta variable y PC2 a una fuente común dominada por renta fija; no se postulan aquí como factores observables exógenos. Los componentes posteriores explican fracciones menores: PC3, por ejemplo, combina una correlación positiva material con TSLA (0.59) y negativa con MU (−0.47), sin una denominación económica unívoca.

En conjunto, la variabilidad conjunta del universo de diez instrumentos se concentra en un número reducido de dimensiones: tres componentes alcanzan el umbral del 80% y cinco el del 90%. El número nominal de activos supera, por tanto, al número de fuentes comunes dominantes identificadas por el PCA en la muestra analizada.
