## Conclusiones del Error Analysis

El principal problema del modelo actual es la predicción de la clase DRAW (F1=0.2829), mientras que HOME (F1=0.6058) y AWAY (F1=0.5556) presentan desempeños razonables.

El análisis muestra que los empates tienden a ocurrir entre equipos más equilibrados en términos de ELO y valor de mercado, aunque las diferencias observadas son moderadas y no permiten una separación clara de la clase DRAW.

Las variables relacionadas con diferencia de puntos recientes y diferencia de goal difference reciente no muestran diferencias relevantes entre clases.

No se identificó una única variable capaz de explicar por sí sola los errores del modelo. Esto sugiere que los empates dependen de combinaciones complejas de variables y no de un único indicador de equilibrio.

Como siguiente paso, se recomienda realizar un análisis de Permutation Importance para identificar qué variables están contribuyendo realmente al rendimiento del modelo y eliminar posibles variables redundantes o ruidosas.

# Perfil de los empates correctamente detectados
## Objetivo

Analizar las diferencias entre los empates correctamente identificados por el modelo y aquellos que fueron clasificados incorrectamente como victoria local o visitante.

## Resultados
| Variable              | DRAW detectados | DRAW perdidos |
| --------------------- | --------------: | ------------: |
| abs_elo_diff          |           38.03 |         86.95 |
| abs_market_value_diff |          15.9 M |        51.6 M |
| balance_score         |            2.78 |          1.84 |
| abs_caps_diff         |            9.21 |         14.30 |
| abs_age_diff          |            1.95 |          2.02 |

## Hallazgos

Los empates correctamente detectados presentan:

menor diferencia Elo
menor diferencia de valor de mercado
menor diferencia de experiencia internacional
mayor equilibrio competitivo

Las variables relacionadas con equilibrio competitivo muestran una separación clara entre empates detectados y empates perdidos.

## Conclusión

El modelo logra identificar empates cuando los equipos presentan niveles similares de calidad según Elo Rating, valor de mercado y experiencia internacional.

La principal fuente de error proviene de empates que ocurren entre equipos aparentemente desiguales, lo que sugiere que todavía existen factores explicativos no representados en las variables actuales.