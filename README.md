# ML en Produccion 
El proyecto intenta generar una forma de predecir resultados en base a las caracteristicas particulares de cada jugador.
La idea inicial es hacer una prediccion con los partidos y fixtures del mundial, sin embargo, dado que las selecciones nacionales no juegan tan seguido, los datos de entrenamiento tendrian que venir de los distintos equipos profecionales en donde juegan los jugadores.
Esto es un problema en si mismo, ya que al jugar 42 selecciones diferentes estamos hablando de jugadores que juegan en ligas de distintos lados del mundo y ademas de distintos niveles de competitividad.
Lo anterior impica un volumen de datos importante, y dado que estos provienen de un scrapper, se manejó la posibilidad de reducir la prediccion a una competicion internacional especifica, ya que esto se podría hacer con u menor volumen de datos.

Objetivo principal

Desarrollar un modelo capaz de predecir el resultado de partidos de fútbol a partir de las características de los jugadores alineados.

Objetivo secundario

Utilizar el modelo como herramienta de simulación para evaluar el impacto potencial de incorporaciones y bajas durante los períodos de transferencias.

Durante la consolidación de datos se identificó que el 2.67% de los partidos carecían de fecha. La mayoría de los registros afectados correspondían a la Süper Lig. Estos registros fueron conservados en el dataset para su análisis posterior.

Durante la auditoría del dataset se identificó que los valores de mercado utilizados provenían de una fotografía estática de los jugadores (players.csv). Se detectó la existencia de una fuente histórica (player_valuations.csv) que permitiría reconstruir el valor de mercado vigente al momento de cada encuentro. Esta mejora fue identificada como trabajo futuro para reducir posibles sesgos temporales.

Se identificó una fuerte correlación (>0.94) entre las variables home_team_market_value y home_team_market_value_mean, así como entre away_team_market_value y away_team_market_value_mean. Tras eliminar las variables promedio, el modelo Random Forest incrementó su F1 Macro de 0.4670 a 0.4709, reduciendo además la dimensionalidad del conjunto de datos.

En este punto ya escribiría una sección de feature selection:

Se calcularon correlaciones entre variables numéricas.
Se detectaron pares con correlación superior a 0.94.
Se eliminaron variables redundantes (*_market_value_mean).
El desempeño mejoró ligeramente (F1 Macro 0.467 → 0.471).
Se conservaron variables correlacionadas con significado futbolístico distinto (points_diff, win_rate_diff) para evitar eliminar señal útil prematuramente.
