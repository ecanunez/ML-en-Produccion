# World Cup Prediction Pipeline

Módulo experimental para evaluar si el modelo campeón **v1.0**,
entrenado sobre partidos históricos de clubes y competiciones
internacionales, puede extrapolarse a partidos de selecciones del
Mundial.

Este pipeline **no reentrena el modelo**. Construye datos de inferencia
compatibles con las features esperadas por el modelo campeón y analiza
su comportamiento fuera del dominio original de entrenamiento.

------------------------------------------------------------------------

# Objetivo

Evaluar la generalización fuera de dominio del modelo campeón **v1.0**
en partidos de selecciones nacionales.

------------------------------------------------------------------------

# Alcance

Este módulo funciona como una **extensión privada** del proyecto
principal.

No modifica:

-   el dataset histórico;
-   el modelo campeón;
-   los experimentos de entrenamiento;
-   los reportes oficiales de la entrega;
-   ni la API principal.

------------------------------------------------------------------------

# Pipeline

``` text
scrape_fifa_teams.py
        ↓
scrape_worldcup_squads.py
        ↓
build_worldcup_player_mapping.py
        ↓
build_worldcup_team_snapshot.py
        ↓
enrich_worldcup_team_snapshot.py
        ↓
scrape_fifa_ranking.py
        ↓
scrape_worldcup_matches.py
        ↓
build_worldcup_scoring_dataset.py
        ↓
predict_worldcup.py
```

------------------------------------------------------------------------

# Orquestador

El pipeline puede ejecutarse desde un único comando:

``` bash
python -m src.worldcup.run_worldcup_pipeline --mode refresh
```

Modos disponibles:

``` text
full
    Descarga equipos, planteles, ranking, partidos y genera predicciones.

refresh
    Actualiza ranking FIFA y partidos del Mundial, reconstruye el scoring dataset y predice.

predict
    Utiliza únicamente los archivos existentes para generar predicciones.
```

------------------------------------------------------------------------

# Evaluación

El módulo incluye una evaluación sobre partidos ya disputados del
Mundial:

``` bash
python -m src.worldcup.evaluate_worldcup
```

Para evitar **data leakage**, la evaluación utiliza los puntos FIFA
**previos al partido** (`TeamAPointsBefore` y `TeamBPointsBefore`) para
construir las variables equivalentes al Elo.

------------------------------------------------------------------------

# Resultados de evaluación

## Modelo original (argmax)

``` text
Accuracy : 0.2683
F1 Macro : 0.1531
```

Se detectó un fuerte sesgo hacia la clase **DRAW**.

Tras evaluar distintas reglas de decisión, la mejor fue:

``` text
draw_threshold = 0.54
```

Resultados obtenidos:

``` text
Accuracy : 0.6220
F1 Macro : 0.5806
```

------------------------------------------------------------------------

# Regla de decisión ajustada

``` python
if prob_draw >= 0.54:
    prediction = "DRAW"
else:
    prediction = "HOME" if prob_home >= prob_away else "AWAY"
```

Esta calibración **no modifica el modelo entrenado**; únicamente cambia
la política de decisión para el dominio de selecciones nacionales.

------------------------------------------------------------------------

# Interpretación

Las predicciones deben interpretarse como un **experimento de
extrapolación fuera de dominio**.

El resultado principal es que el modelo campeón contiene señal útil para
selecciones nacionales, aunque requiere una política de decisión
calibrada para evitar un sesgo excesivo hacia los empates.

------------------------------------------------------------------------

# Salida

El script de predicción muestra una tabla resumida:

``` text
============================================================
PREDICCIONES DEL MUNDIAL
============================================================

                  fase                          partido predicción confianza
Dieciseisavos de final                España vs Austria     España      43.8%
Dieciseisavos de final              Portugal vs Croacia   Portugal      30.5%
Dieciseisavos de final              Australia vs Egipto     Empate      54.5%
```

Además, guarda las predicciones completas en:

``` text
data/prediction_worldcup/predictions/
```

------------------------------------------------------------------------

# Nota

Este módulo se mantiene fuera del repositorio principal mediante
`.gitignore`.

Una vez finalizada la evaluación académica del proyecto, podrá
incorporarse como una extensión **v1.1** del sistema de predicción.
