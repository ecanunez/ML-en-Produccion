# Model History

## Objetivo

Evaluar distintos algoritmos de clasificación multiclase para la predicción de resultados de partidos internacionales de fútbol:

* HOME
* DRAW
* AWAY

La métrica principal utilizada es **F1 Macro**, ya que el problema presenta desbalance entre clases y se busca un rendimiento equilibrado para las tres categorías.

---

# Baseline Inicial

Dataset: `training_dataset_fe_v1`

| Modelo              | Features | Accuracy | F1 Macro |
| ------------------- | -------: | -------: | -------: |
| Logistic Regression |       61 |   0.5361 |   0.3993 |
| Random Forest       |       61 |   0.5262 |   0.4876 |

### Observaciones

* Logistic Regression obtuvo mayor accuracy.
* Random Forest logró una mejora significativa en F1 Macro.
* Se decidió continuar la experimentación utilizando modelos basados en árboles.

---

# Feature Engineering v1

Se incorporaron variables derivadas de:

### Valor de mercado

* Diferencias por posición
* Diferencias absolutas
* Indicadores de balance

### Rendimiento reciente

* Puntos últimos 5 partidos
* Win rate
* Goal difference

### Elo Rating

* Elo local
* Elo visitante
* Diferencia Elo

### Perfil de plantel

* Edad promedio
* Altura promedio
* Valor promedio
* Internacionalidades
* Goles internacionales

Número final de variables:

**72 features**

---

# Evaluación Holdout (80/20)

Dataset:

`training_dataset.parquet`

Fecha dataset:

`2026-06-20 15:27:30`

## Random Forest Tuned

Parámetros:

* n_estimators = 500
* max_depth = 10
* min_samples_leaf = 5
* class_weight = balanced

Resultados:

| Accuracy | F1 Macro |
| -------: | -------: |
|   0.5147 |   0.4830 |

---

## HistGradientBoosting

Parámetros:

* learning_rate = 0.05
* max_depth = 6
* max_iter = 300

Resultados:

| Accuracy | F1 Macro |
| -------: | -------: |
|   0.5369 |   0.4094 |

---

## XGBoost

Parámetros:

* n_estimators = 500
* max_depth = 6
* learning_rate = 0.05
* subsample = 0.8
* colsample_bytree = 0.8

Resultados:

| Accuracy | F1 Macro |
| -------: | -------: |
|   0.5286 |   0.4379 |

---

## LightGBM

Parámetros:

* n_estimators = 500
* learning_rate = 0.05
* max_depth = 6

Resultados:

| Accuracy | F1 Macro |
| -------: | -------: |
|   0.5290 |   0.4509 |

---

# Validación Cruzada (5-Fold Stratified)

Métrica:

**F1 Macro**

| Modelo             | Mean F1 |    Std |
| ------------------ | ------: | -----: |
| RandomForest_Tuned |  0.4759 | 0.0115 |
| LogisticRegression |  0.4693 | 0.0068 |
| LightGBM           |  0.4406 | 0.0061 |
| XGBoost            |  0.4334 | 0.0104 |

---

# Conclusiones

## Mejor modelo actual

**RandomForest_Tuned**

Resultados:

* Holdout F1 Macro: 0.4830
* Cross Validation F1 Macro: 0.4759

Presenta:

* Mejor rendimiento general
* Buena estabilidad entre folds
* Menor riesgo de sobreajuste

## Hallazgos relevantes

* XGBoost no superó a Random Forest.
* LightGBM mejoró ligeramente respecto a XGBoost.
* Logistic Regression sigue siendo un baseline competitivo.
* HistGradientBoosting obtuvo el peor F1 Macro de los modelos evaluados.
* Las nuevas variables de Elo, forma reciente y perfil de plantel aportaron mejora incremental al desempeño.

## Próximos pasos (Fase 4)

Posibles líneas de trabajo:

1. Feature Selection formal.
2. Eliminación de variables redundantes.
3. Hyperparameter Tuning avanzado.
4. Calibración de probabilidades.
5. Ensemble de modelos.
6. Optimización específica para la clase DRAW.

# Error Analysis (2026-06-21)
Matriz de confusion
| Real \ Pred | HOME | DRAW | AWAY |
| ----------- | ---: | ---: | ---: |
| HOME        |  663 |  228 |  226 |
| DRAW        |  231 |  171 |  220 |
| AWAY        |  158 |  160 |  463 |

Principales errores
| Error       | Casos |
| ----------- | ----: |
| DRAW → HOME |   231 |
| HOME → DRAW |   228 |
| HOME → AWAY |   226 |
| DRAW → AWAY |   220 |
| AWAY → DRAW |   160 |
| AWAY → HOME |   158 |

## Hallazgo Principal
La clase más difícil de predecir continúa siendo DRAW.

El análisis mostró que el modelo identifica correctamente empates cuando existe un alto nivel de equilibrio competitivo entre los equipos.

Las variables más asociadas a empates correctamente detectados fueron:

abs_elo_diff
abs_market_value_diff
abs_caps_diff
balance_score

Esto valida la utilidad de las variables de balance incorporadas durante Feature Engineering v2.

## Próximos pasos (Fase 4)

1. Error Analysis específico de DRAW.
2. Comparación DRAW_TO_HOME vs DRAW_TO_AWAY.
3. Error Analysis utilizando Top40 Features.
4. Permutation Importance.
5. Recursive Feature Elimination (RFE).
6. Nuevas variables orientadas a empates inesperados.

# Feature Selection y Nuevo Baseline

## Fecha

2026-06-21

---

## Objetivo

Evaluar si la eliminación de variables de baja importancia permite mejorar la capacidad de generalización del modelo.

---

## Metodología

Se utilizaron las importancias obtenidas mediante Random Forest Tuned para ordenar las variables.

Posteriormente se entrenó el mismo modelo utilizando distintos subconjuntos de features:

| Features | F1 Macro |
| -------: | -------: |
|    Top10 |   0.4724 |
|    Top20 |   0.4750 |
|    Top30 |   0.4760 |
|    Top40 |   0.4870 |
|    Top50 |   0.4798 |
| All (72) |   0.4830 |

El mejor resultado se obtuvo utilizando únicamente las 40 variables más relevantes.

---

## Error Analysis Top40

Se repitió el análisis de errores utilizando únicamente las 40 variables seleccionadas.

### Resultados

| Métrica         | 72 Features |  Top40 |
| --------------- | ----------: | -----: |
| Accuracy        |      0.5147 | 0.5163 |
| F1 Macro        |      0.4830 | 0.4860 |
| Precision Macro |      0.4818 | 0.4850 |
| Recall Macro    |      0.4871 | 0.4897 |

### Clase DRAW

| Métrica   | 72 Features |  Top40 |
| --------- | ----------: | -----: |
| Precision |      0.3059 | 0.3073 |
| Recall    |      0.2749 | 0.2846 |
| F1        |      0.2896 | 0.2955 |

La reducción de dimensionalidad mejoró especialmente la detección de empates, reduciendo errores de clasificación y aumentando el recall de la clase DRAW.

---

## Nuevo Mejor Modelo

### Random Forest Tuned Top40

Parámetros:

* n_estimators = 500
* max_depth = 10
* min_samples_leaf = 5
* min_samples_split = 2
* class_weight = balanced

Resultados:

| Accuracy | F1 Macro |
| -------: | -------: |
|   0.5163 |   0.4860 |

---

## Conclusiones

1. El mejor desempeño no se obtiene utilizando todas las variables disponibles.
2. La eliminación de variables redundantes mejora la capacidad de generalización.
3. La información predictiva del problema se encuentra concentrada en aproximadamente 40 variables.
4. Los principales errores continúan asociados a la predicción de empates.
5. Los empates correctamente detectados corresponden mayoritariamente a partidos equilibrados en términos de Elo, valor de mercado y experiencia internacional.

---

## Estado del Proyecto

### Baseline Oficial

**Random Forest Tuned Top40**

* Features: 40
* Accuracy: 0.5163
* F1 Macro: 0.4860

Este modelo pasa a ser el nuevo punto de referencia para la Fase 4.

## 2026-06-22 — Random Forest Tuned + Top30 Features

### Configuración

Modelo:

* RandomForestClassifier

Parámetros:

* n_estimators = 500
* max_depth = 10
* min_samples_leaf = 5
* min_samples_split = 2
* class_weight = balanced

Features:

* Top30 seleccionadas automáticamente mediante Feature Importance (RF v2)

### Resultados

| Métrica         |  Valor |
| --------------- | -----: |
| Accuracy        | 0.5143 |
| F1 Macro        | 0.4858 |
| Precision Macro | 0.4851 |
| Recall Macro    | 0.4890 |

### Resultados por clase

| Clase | Precision | Recall |     F1 |
| ----- | --------: | -----: | -----: |
| AWAY  |    0.5145 | 0.5890 | 0.5493 |
| DRAW  |    0.3033 | 0.2926 | 0.2979 |
| HOME  |    0.6374 | 0.5855 | 0.6104 |

### Hallazgos

* Resultado prácticamente equivalente al modelo Top40.
* Se confirma que gran parte de la señal predictiva está concentrada en aproximadamente 30 variables.
* El modelo mantiene un desempeño competitivo utilizando menos variables.
* La selección automática de variables supera al uso de las features disponibles.
* La mejora más importante se observa en la clase DRAW.
* Se confirma que una parte importante de la señal predictiva se concentra en aproximadamente 30 variables.

Estado:

✅ Modelo líder actual.


# Actualización Dataset v2 (2026-06-22)

## Objetivo

Reevaluar el pipeline completo tras la incorporación de nuevas variables derivadas de:

* draw_features.parquet
* interaction_features.parquet
* nuevas transformaciones Elo

---

## Dataset actualizado

| Métrica              |              Valor |
| -------------------- | -----------------: |
| Partidos             |             12,599 |
| Features disponibles |                 99 |
| Clases               | HOME / DRAW / AWAY |

---

## Nuevas familias de variables

### draw_features.parquet

Variables diseñadas para detectar partidos equilibrados:

* elo_draw_zone
* market_draw_zone
* experience_draw_zone
* ultra_balanced_match
* draw_candidate_score

---

### interaction_features.parquet

Variables de interacción entre señales predictivas:

* elo_market_interaction
* elo_caps_interaction
* attack_strength_interaction
* value_per_elo
* caps_per_elo

---

## Permutation Importance

Las variables con mayor importancia fueron:

| Variable               | Importance |
| ---------------------- | ---------: |
| home_elo               |     0.0065 |
| caps_per_elo           |     0.0062 |
| elo_favorite_strength  |     0.0060 |
| elo_draw_proxy         |     0.0060 |
| elo_caps_interaction   |     0.0057 |
| home_avg_player_value  |     0.0054 |
| elo_market_interaction |     0.0046 |

### Hallazgo

Las nuevas variables derivadas de Elo e interacciones aparecen sistemáticamente entre las más importantes del modelo.

Esto indica que las transformaciones no lineales contienen información predictiva adicional respecto a las variables originales.

---

# Correlation Analysis

Se realizó un análisis de correlaciones utilizando todas las variables disponibles.

Principales correlaciones detectadas:

| Variable A             | Variable B                 | Correlación |
| ---------------------- | -------------------------- | ----------: |
| home_players_found     | home_profile_players_found |      0.9997 |
| away_players_found     | away_profile_players_found |      0.9996 |
| points_diff            | win_rate_diff              |      0.9536 |
| home_team_market_value | home_avg_player_value      |      0.9471 |
| away_team_market_value | away_avg_player_value      |      0.9469 |
| home_points_last5      | home_win_rate_last5        |      0.9426 |
| away_points_last5      | away_win_rate_last5        |      0.9368 |

### Conclusión

Existen variables altamente correlacionadas, pero la eliminación automática de estas variables no se consideró prioritaria dado que los modelos basados en árboles suelen tolerar bien la multicolinealidad.

Se decidió continuar utilizando Feature Selection basada en importancia predictiva.

---

# Feature Selection v2

## Metodología

Se utilizó Random Forest Tuned para generar un ranking de importancia de variables.

Posteriormente se evaluaron distintos subconjuntos de features.

### Resultados

| Features | F1 Macro |
| -------: | -------: |
|    Top10 |   0.4730 |
|    Top20 |   0.4670 |
|    Top30 |   0.4858 |
|    Top40 |   0.4806 |
|    Top50 |   0.4785 |
|    Top60 |   0.4793 |
| All (87) |   0.4750 |

---

## Hallazgos

1. Utilizar todas las variables disponibles no produce el mejor resultado.
2. La información predictiva está concentrada en un subconjunto reducido de variables.
3. El mejor desempeño se obtuvo utilizando únicamente las 30 variables más importantes.
4. Las nuevas variables Elo e interacciones aparecen repetidamente dentro del Top30.

---

# Reevaluación del Baseline

Se evaluó nuevamente Feature Selection tras la incorporación de nuevas variables derivadas de Elo e interacciones.

Aunque el subconjunto Top30 logró un rendimiento muy similar al Top40 histórico, no consiguió superarlo.

Por lo tanto, el baseline oficial del proyecto continúa siendo:

## Random Forest Tuned + Top40 Features

Accuracy: 0.5163
F1 Macro: 0.4860

### Parámetros

* n_estimators = 500
* max_depth = 10
* min_samples_leaf = 5
* min_samples_split = 2
* class_weight = balanced

### Resultados

| Métrica         |  Valor |
| --------------- | -----: |
| Accuracy        | 0.5143 |
| F1 Macro        | 0.4858 |
| Precision Macro | 0.4851 |
| Recall Macro    | 0.4890 |

---

## Resultados por clase

| Clase | Precision | Recall |     F1 |
| ----- | --------: | -----: | -----: |
| AWAY  |    0.5145 | 0.5890 | 0.5493 |
| DRAW  |    0.3033 | 0.2926 | 0.2979 |
| HOME  |    0.6374 | 0.5855 | 0.6104 |

---

## Top Features del modelo

1. elo_away_win_prob
2. elo_home_win_prob
3. elo_diff
4. market_value_diff
5. value_per_elo
6. elo_market_interaction
7. DEF_value_diff
8. caps_diff
9. home_avg_player_value
10. elo_caps_interaction

---

## Conclusiones

* Las transformaciones derivadas de Elo aportan información predictiva relevante.
* Las variables de interacción se consolidan entre las más importantes del modelo.
* El modelo continúa mostrando dificultades para la predicción de empates.
* El rendimiento máximo actual se obtiene utilizando un subconjunto reducido de variables.
* Random Forest sigue superando a XGBoost y LightGBM en F1 Macro.

---

# Estado Actual del Proyecto

## Modelo líder

Random Forest Tuned + Top40 Features

Modelo alternativo:

Random Forest Tuned + Top30 Features

F1 Macro: 0.4858

Ofrece un rendimiento prácticamente idéntico utilizando 25% menos variables.

### Métricas

* Accuracy: 0.5143
* F1 Macro: 0.4858

### Features utilizadas

30

### Dataset

99 features disponibles

### Estado

✅ Baseline oficial actual del proyecto.

Validación Cruzada Top30 (2026-06-22)

Modelo:
Random Forest Tuned Top30

Resultados:

Mean F1 Macro: 0.4793
Std: 0.0106

Fold Scores:
0.4765
0.4868
0.4912
0.4606
0.4817

Conclusión:

El desempeño observado en holdout se mantiene bajo validación cruzada, indicando una capacidad de generalización adecuada y ausencia de sobreajuste significativo.

# Ensemble Experiment (2026-06-22)

## Soft Voting Ensemble

Modelos:

* Random Forest Tuned Top30
* Logistic Regression

Método:

* Soft Voting

### Resultados

| Métrica         | Valor |
| --------------- | ----: |
| Accuracy        | 0.5290 |
| F1 Macro        | 0.4521 |
| Precision Macro | 0.4630 |
| Recall Macro    | 0.4726 |

### Conclusión

Aunque el ensemble incrementó la accuracy respecto al modelo base, produjo una caída significativa en F1 Macro.

La principal causa fue la reducción del recall de la clase DRAW:

* RF Top30: Recall DRAW = 0.2926
* Ensemble: Recall DRAW = 0.1190

Dado que el objetivo principal del proyecto es maximizar F1 Macro y mejorar la detección de empates, el enfoque de Soft Voting fue descartado.

Estado:

❌ Evaluado y descartado.

# Probability Calibration (2026-06-22)

## Objetivo

Evaluar si la calibración de probabilidades permite mejorar la detección de empates y aumentar el F1 Macro del modelo Random Forest Top30.

## Configuración

Modelo base:

* Random Forest Tuned Top30

Calibración:

* CalibratedClassifierCV
* method = isotonic
* cv = 5

## Resultados

| Métrica         |  Valor |
| --------------- | -----: |
| Accuracy        | 0.5417 |
| F1 Macro        | 0.4066 |
| Precision Macro | 0.4823 |
| Recall Macro    | 0.4678 |

## Clase DRAW

| Métrica   |  Valor |
| --------- | -----: |
| Precision | 0.3750 |
| Recall    | 0.0048 |
| F1        | 0.0095 |

## Conclusión

La calibración incrementó la accuracy, pero eliminó prácticamente la capacidad de detectar empates.

El recall de la clase DRAW cayó desde 0.2926 hasta 0.0048.

Dado que el objetivo principal del proyecto es maximizar F1 Macro y mejorar la detección de empates, la calibración de probabilidades fue descartada.

Estado:

❌ Evaluada y descartada.

# Stacking Ensemble (2026-06-22)

## Objetivo

Combinar la capacidad de generalización de Logistic Regression con la capacidad de modelar relaciones no lineales de Random Forest.

## Configuración

Modelos base:

* Random Forest Tuned
* Logistic Regression

Meta-modelo:

* Logistic Regression

Método:

* StackingClassifier
* stack_method = predict_proba
* cv = 5

Features:

* Top30 seleccionadas mediante Feature Importance

## Resultados

| Métrica         |  Valor |
| --------------- | -----: |
| Accuracy        | 0.5123 |
| F1 Macro        | 0.4915 |
| Precision Macro | 0.4934 |
| Recall Macro    | 0.4934 |

## Resultados por clase

| Clase | Precision | Recall |     F1 |
| ----- | --------: | -----: | -----: |
| AWAY  |    0.5256 | 0.5787 | 0.5509 |
| DRAW  |    0.3032 | 0.3392 | 0.3202 |
| HOME  |    0.6515 | 0.5622 | 0.6036 |

## Hallazgos

* Mejor F1 Macro obtenido hasta la fecha.
* Incremento significativo en la detección de empates.
* La mejora proviene principalmente del aumento del recall de la clase DRAW.
* El stacking logra combinar patrones lineales y no lineales presentes en el dataset.

## Estado

✅ Nuevo modelo líder del proyecto.

# Ensemble Experiments (2026-06-22)

## Objetivo

Evaluar si la combinación de modelos permite mejorar el desempeño
del Random Forest Top30.

---

# Baseline Oficial Actual

## Modelo líder

Stacking Ensemble Top30

### Resultados Holdout

Accuracy: 0.5123

F1 Macro: 0.4915

### Resultados Cross Validation

Mean F1 Macro: 0.4810

Std: 0.0090

### Conclusión

El modelo Stacking Ensemble Top30 presenta el mejor desempeño
global del proyecto.

La mejora respecto a Random Forest Top30 es moderada pero
consistente tanto en Holdout como en Validación Cruzada.

Además, mejora la capacidad de detección de empates (DRAW),
que continúa siendo la clase más difícil del problema.

Estado:

✅ Baseline oficial actual del proyecto.

# Resumen

| Modelo         | Holdout F1 |      CV F1 |
| -------------- | ---------: | ---------: |
| RF Top40       |     0.4860 |          — |
| RF Top30       |     0.4858 |     0.4793 |
| Stacking Top30 | **0.4915** | **0.4810** |
