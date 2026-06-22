# Model Selection Report

## Objetivo

Evaluar distintos algoritmos de clasificación multiclase para la predicción de resultados de partidos internacionales:

* HOME
* DRAW
* AWAY

La métrica principal utilizada fue **F1 Macro**, debido al desbalance existente entre clases.

---

## Dataset

Dataset utilizado:

training_dataset.parquet

Características:

* Observaciones: 12,599
* Features: 72
* Clases:

  * HOME
  * DRAW
  * AWAY

Split de entrenamiento:

* Train: 80%
* Test: 20%
* Stratified Split
* random_state=42

---

## Benchmark Inicial

| Modelo               | Accuracy | F1 Macro |
| -------------------- | -------: | -------: |
| Baseline Dummy       |   0.4433 |   0.2047 |
| Logistic Regression  |   0.4782 |   0.4702 |
| Random Forest        |   0.5341 |   0.4176 |
| Random Forest Tuned  |   0.5147 |   0.4830 |
| HistGradientBoosting |   0.5349 |   0.4249 |

Observaciones:

* Logistic Regression mostró una performance muy sólida.
* El Random Forest sin ajustar tuvo dificultades para predecir empates.
* El ajuste de hiperparámetros mejoró significativamente el F1 Macro.
* HistGradientBoosting no superó al Random Forest Tuned.

---

## Modelos Boosting Adicionales

Se evaluaron implementaciones externas de boosting.

### XGBoost

| Métrica  |  Valor |
| -------- | -----: |
| Accuracy | 0.5286 |
| F1 Macro | 0.4379 |

### LightGBM

| Métrica  |  Valor |
| -------- | -----: |
| Accuracy | 0.5290 |
| F1 Macro | 0.4509 |

Observaciones:

* LightGBM superó a XGBoost.
* Ninguno de los modelos boosting logró superar al Random Forest Tuned.

---

## Validación Cruzada

Configuración:

* StratifiedKFold
* 5 folds
* shuffle=True
* random_state=42
* scoring=f1_macro

### Resultados

| Modelo             | Mean F1 Macro |    Std |
| ------------------ | ------------: | -----: |
| RandomForest_Tuned |        0.4759 | 0.0115 |
| LogisticRegression |        0.4693 | 0.0068 |
| LightGBM           |        0.4406 | 0.0061 |
| XGBoost            |        0.4334 | 0.0104 |

| Modelo               | Holdout F1 |  CV F1 |
| -------------------- | ---------: | -----: |
| RandomForest_Tuned   |     0.4830 | 0.4759 |
| LogisticRegression   |     0.4702 | 0.4693 |
| LightGBM             |     0.4509 | 0.4406 |
| XGBoost              |     0.4379 | 0.4334 |
| HistGradientBoosting |     0.4249 |      — |

---

## Modelo Seleccionado

Modelo ganador:

RandomForest_Tuned

Configuración:

* n_estimators=500
* max_depth=10
* min_samples_leaf=5
* min_samples_split=2
* class_weight=balanced

Resultado final:

* CV F1 Macro: 0.4759

Justificación:

* Mejor rendimiento promedio en validación cruzada.
* Rendimiento consistente entre folds.
* Supera a Logistic Regression, LightGBM y XGBoost.

---

## Conclusiones

La ingeniería de variables realizada tuvo un impacto significativo en el desempeño de los modelos.

Las variables relacionadas con:

* Elo Rating
* Valor de mercado
* Forma reciente
* Diferencias entre equipos
* Variables de balance competitivo

aportaron suficiente capacidad predictiva para que modelos basados en árboles simples superaran a algoritmos boosting más complejos.

---

## Próxima Fase

Fase 4: Ingeniería Avanzada de Variables

Líneas de trabajo:

* Nuevas variables Elo
* Rolling windows más extensas
* Variables ofensivas y defensivas
* Strength of Schedule
* Análisis de errores del modelo seleccionado
* Selección avanzada de variables
