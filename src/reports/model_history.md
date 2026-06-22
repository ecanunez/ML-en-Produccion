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
