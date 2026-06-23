# Inference Pipeline

## Objetivo

Realizar predicciones online y batch utilizando el modelo campeón exportado.

---

## Estructura

models/
└── champions/
    └── v1.0_model_champion/
        ├── model.joblib
        ├── metadata.json
        ├── top30_features.csv
        └── README.md

src/
└── inference/
    └── predict.py

---

## Modelo utilizado

Champion Model:

v1.0_model_champion

Arquitectura:

Stacking Ensemble

Base Models:

* Random Forest Tuned
* Logistic Regression

Meta Model:

* Logistic Regression

---

## Features utilizadas

30 variables seleccionadas mediante Feature Selection v2.

Las variables esperadas por el modelo se cargan automáticamente desde:

models/champions/v1.0_model_champion/top30_features.csv

---

## Predicción

El módulo:

src/inference/predict.py

realiza:

1. Carga del modelo exportado
2. Carga automática de features
3. Validación de columnas
4. Predicción de clase
5. Predicción de probabilidades

Salida:

| prediction | prob_away | prob_draw | prob_home |
| ---------- | --------: | --------: | --------: |
| AWAY       |    0.7399 |    0.1886 |    0.0716 |
| DRAW       |    0.2421 |    0.3821 |    0.3758 |

---

## Casos de uso

### Online Prediction

Predicción de un partido individual.

Entrada:

1 observación

Salida:

Resultado esperado + probabilidades.

---

### Batch Prediction

Predicción masiva de múltiples partidos.

Entrada:

DataFrame con N observaciones.

Salida:

DataFrame con predicciones y probabilidades.

---

## Estado

✅ Inference Pipeline funcional

Próximo paso:

API REST para serving de predicciones.