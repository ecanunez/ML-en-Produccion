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