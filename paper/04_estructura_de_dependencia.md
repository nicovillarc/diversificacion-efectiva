## 4. Segunda capa del diagnóstico: ¿cómo se mueven los activos?

**Pregunta:** ¿Diez instrumentos representan diez comportamientos independientes?

Tras examinar la dispersión del capital, el diagnóstico incorpora la estructura de dependencia entre retornos. Se estiman correlaciones de Pearson sobre los retornos logarítmicos diarios de la ventana fija 2016-01-01 a 2026-06-30 (\(T = 2{,}636\) observaciones).

**Resultados agregados**

| Métrica | Valor |
|---------|-------|
| Correlación media (pares off-diagonal) | 0.34 |
| Correlación media intra–renta variable | 0.63 |
| Correlación media intra–renta fija | 0.86 |
| Correlación media entre clases | −0.03 |
| Mínimo / máximo entre pares | −0.16 / 0.93 |
| Enlaces con \(\lvert\rho\rvert \ge 0.60\) | 15 |

**Figura 3.** Matriz de correlación de retornos.

La matriz revela dos bloques de dependencia elevada. En renta variable, las correlaciones intra-clase son en general altas: SPY–QQQ alcanza 0.93 y QQQ–SMH 0.88, con vínculos fuertes también entre SMH, NVDA, MU y AAPL. En renta fija, BND, IEF y TLT forman un bloque aún más compacto (correlaciones entre 0.80 y 0.91). En cambio, las correlaciones cruzadas entre renta variable y renta fija se concentran cerca de cero, con valores negativos moderados entre los Treasuries (IEF, TLT) y varios equity.

**Figura 4.** Red de correlaciones (\(\lvert\rho\rvert \ge 0.60\)).

El grafo confirma visualmente dos clusters separados por clase de activo y la ausencia de enlaces cruzados por encima del umbral. TSLA aparece como nodo aislado: sus correlaciones con el resto del universo permanecen por debajo de 0.60 (máximo 0.57 con QQQ).

En conjunto, los diez instrumentos no se comportan como diez fuentes independientes de variación. La dependencia es alta *dentro* de cada clase y baja *entre* clases, lo que anticipa superposición de exposiciones —en particular dentro del bloque equity tecnológico/semiconductor y dentro de la renta fija— sin eliminar el potencial diversificador de la separación 60/40. La cuantificación de esa redundancia en términos de riesgo se aborda en la capa siguiente.
