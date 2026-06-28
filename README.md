# ML-en-Produccion

Sistema de Machine Learning para la predicción de resultados de partidos de fútbol profesional utilizando datos históricos, información de plantillas y variables derivadas de jugadores y equipos.

El proyecto implementa el ciclo completo de un sistema de Machine Learning en producción, incluyendo:

* recolección automática de datos mediante scraping;
* construcción y procesamiento de datasets;
* ingeniería de variables;
* entrenamiento y evaluación de modelos;
* selección y exportación del modelo campeón;
* generación de predicciones para partidos futuros.

---

# Estado del proyecto

**Versión actual:** **v1.0**

| Componente          | Estado |
| ------------------- | :----: |
| Data Collection     |    ✅   |
| Data Processing     |    ✅   |
| Feature Engineering |    ✅   |
| Model Training      |    ✅   |
| Champion Model      |    ✅   |
| Historical Pipeline |    ✅   |
| Inference Pipeline  |    ✅   |
| Batch Prediction    |    ✅   |
| API REST            |    ⏳   |

---

# Modelo campeón

El modelo actualmente seleccionado es un **Stacking Ensemble**, entrenado utilizando el conjunto de **Top 30 Features** obtenido durante la etapa de selección de variables.

Resultados obtenidos sobre el conjunto de test:

| Métrica         |      Valor |
| --------------- | ---------: |
| Accuracy        | **0.5123** |
| F1 Macro        | **0.4915** |
| Precision Macro | **0.4934** |
| Recall Macro    | **0.4934** |

El modelo se exporta como un artefacto autocontenido:

```text
models/champion_model.pkl
```

---

# Arquitectura

El proyecto está organizado alrededor de dos pipelines independientes.

## Pipeline histórico

```text
Raw Data
    ↓
Data Processing
    ↓
Feature Engineering
    ↓
Training Dataset
    ↓
Model Training
    ↓
Champion Model
```

## Pipeline de inferencia

```text
Upcoming Matches
        ↓
Team Squads
        ↓
Team Features
        ↓
Player Features
        ↓
Scoring Dataset
        ↓
Champion Model
        ↓
Predictions
```

---

# Ejecución

## Reconstruir completamente el modelo

```bash
python -m src.pipelines.run_historical_pipeline
```

Este pipeline:

* consolida los datos históricos;
* construye el dataset de entrenamiento;
* genera todas las variables;
* entrena el modelo;
* exporta el modelo campeón.

---

## Generar predicciones para partidos futuros

```bash
python -m src.pipelines.run_inference_pipeline
```

Este pipeline:

* obtiene los próximos partidos;
* descarga las plantillas actuales;
* construye las variables de inferencia;
* genera el scoring dataset;
* produce las predicciones finales.

---

## Ejecutar únicamente el modelo de inferencia

```bash
python -m src.inference.predict
```

---

# Principales outputs

Durante la ejecución del proyecto se generan, entre otros, los siguientes archivos:

```text
data/processed/

training_dataset.parquet
scoring_dataset.parquet
predictions.csv

models/

champion_model.pkl
```

---

# Documentación

La documentación técnica del proyecto se encuentra en la carpeta:

```text
docs/
```

Documentos disponibles:

* **README.md** — índice de la documentación.
* **architecture.md** — arquitectura general del sistema.
* **project_structure.md** — organización del repositorio.
* **pipelines.md** — descripción de los pipelines.
* **model_card.md** — documentación del modelo campeón.

Los reportes generados durante el desarrollo del proyecto pueden consultarse en:

```text
src/reports/
```

---

# Próximos pasos

Las principales líneas de evolución previstas son:

* incorporación de nuevas ligas nacionales fuera de Europa;
* ampliación de competiciones internacionales;
* actualización dinámica del ELO durante la inferencia;
* incorporación de estadísticas recientes por jugador;
* simulación de transferencias y modificaciones de plantillas;
* calibración de probabilidades;
* despliegue mediante una API REST;
* contenerización con Docker.

---

# Licencia

Proyecto desarrollado con fines académicos y de investigación.
