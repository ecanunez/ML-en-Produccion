# Matching de Jugadores y Features de Perfil

## Motivación

Uno de los objetivos del proyecto es permitir, en etapas futuras, la simulación de modificaciones en las plantillas de los equipos.

Para ello no resulta suficiente trabajar únicamente con variables agregadas a nivel club, sino que es necesario vincular los jugadores presentes en las alineaciones con información individual proveniente de Transfermarkt.

---

## Construcción del Player Mapping

Las alineaciones obtenidas mediante scraping contienen únicamente nombres de jugadores.

Ejemplo:

```text
Herrera
García
Cruz
Moncayola
Ávila
```

Por otro lado, la base de Transfermarkt contiene identificadores únicos para cada jugador:

```text
player_id
player_name
market_value
position
date_of_birth
international_caps
...
```

Se desarrolló un proceso de matching para vincular ambos universos.

### Estrategias utilizadas

1. Exact Match

Coincidencia exacta entre nombre normalizado y nombre oficial del jugador.

2. Matching por apellidos

Se construyeron representaciones utilizando:

* último apellido
* últimos dos apellidos
* últimos tres apellidos

para capturar diferencias en la forma de nombrar a los futbolistas.

3. Prefix Match

Se implementó soporte para formatos abreviados:

```text
J. Álvarez
M. Gómez
```

buscando coincidencias por prefijo sobre distintas variantes del nombre.

---

## Restricción temporal

Para reducir ambigüedades se limitó el universo de búsqueda a jugadores activos en temporadas recientes.

```python
last_season >= 2022
```

Dado que el dataset de partidos comienza en 2022, esta restricción eliminó miles de futbolistas históricos que generaban múltiples coincidencias posibles.

La cobertura del matching mejoró significativamente tras aplicar este filtro.

---

## Cobertura obtenida

Resultado final:

```text
Jugadores mapeados:
≈ 7 titulares por equipo

Cobertura promedio:
home_profile_players_found ≈ 6.91
away_profile_players_found ≈ 6.90
```

Esto implica que aproximadamente el 63% de los futbolistas presentes en cada alineación pudieron vincularse exitosamente con su perfil individual.

---

## Features de perfil de jugador

A partir de los jugadores mapeados se construyeron variables agregadas para cada alineación.

### Edad promedio

```text
home_avg_age
away_avg_age
```

Calculada utilizando la fecha de nacimiento de cada futbolista.

### Experiencia internacional promedio

```text
home_avg_caps
away_avg_caps
```

Basada en la cantidad de partidos disputados con selecciones nacionales absolutas.

### Cobertura del matching

```text
home_profile_players_found
away_profile_players_found
```

Cantidad de jugadores identificados correctamente dentro de cada alineación.

---

## Variables derivadas

Posteriormente se generaron variables diferenciales entre ambos equipos:

```text
age_diff
caps_diff
profile_players_found_diff
```

donde:

```text
age_diff
=
home_avg_age
-
away_avg_age
```

```text
caps_diff
=
home_avg_caps
-
away_avg_caps
```

Estas variables buscan capturar diferencias estructurales entre las alineaciones más allá del valor de mercado o la fortaleza histórica de los equipos.

---

## Importancia para futuras etapas

Esta arquitectura permite incorporar nuevas características individuales sin modificar el pipeline principal.

Por ejemplo:

* pie dominante
* altura
* posición
* experiencia internacional
* goles internacionales
* minutos disputados
* valor de mercado histórico

Además habilita uno de los objetivos secundarios del proyecto:

simular el impacto potencial de fichajes, ventas o cambios de alineación sobre las probabilidades estimadas por el modelo.


# Trabajo futuro

## Modelado

- XGBoost
- LightGBM
- CatBoost
- Calibration de probabilidades

## Features

- Valores de mercado históricos
- Estadísticas recientes por jugador
- Métricas local/visitante
- Historial de lesiones
- Experiencia internacional avanzada

## Simulación de plantillas

La arquitectura actual permite reemplazar jugadores individuales dentro de una alineación y recalcular automáticamente las features agregadas del equipo.

Esto habilita escenarios de simulación para:

- incorporaciones
- transferencias
- lesiones
- cambios tácticos
- alineaciones alternativas

## Validación de inferencia

El modelo fue validado mediante carga desde artefacto serializado (`model.joblib`) utilizando el módulo:

src/inference/predict.py

Resultados:

* Modelo cargado correctamente.
* Features Top30 recuperadas desde `top30_features.csv`.
* Predicciones y probabilidades generadas exitosamente.
* Pipeline listo para consumo por scripts batch o API futura.

# Estado Actual

Fase 1 — Data Collection ✅

Fase 2 — Feature Engineering ✅

Fase 3 — Model Training & Benchmarking ✅

Fase 4 — Feature Selection & Ensemble Models ✅

Fase 5 — Champion Model Export ✅

Fase 6 — Inference Pipeline ✅

Fase 7 — API Deployment ⏳

## Estado del Proyecto

### Versión actual

v1.0

### Mejor modelo

Random Forest Optimizado

### Métrica principal

F1 Macro: 0.472

### Estado

✅ Dataset construido

✅ Ingeniería de variables

✅ Selección de características

✅ Optimización de hiperparámetros

✅ Pipeline de inferencia

⏳ API REST

⏳ Scoring de partidos futuros

⏳ Deployment
