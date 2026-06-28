# ⚽ Football Match Prediction System

Sistema de Machine Learning para la predicción de resultados de partidos de fútbol utilizando datos tabulares construidos mediante scraping de Transfermarkt.

El proyecto fue desarrollado con foco en buenas prácticas de Machine Learning en producción, incluyendo construcción del dataset, ingeniería de variables, selección de características, optimización del modelo, pipelines reproducibles, API de inferencia y despliegue mediante Docker.

---

# Estado del proyecto

| Componente          | Estado |
| ------------------- | :----: |
| Dataset             |    ✅   |
| EDA                 |    ✅   |
| Feature Engineering |    ✅   |
| Feature Selection   |    ✅   |
| Model Benchmark     |    ✅   |
| Champion Model      |    ✅   |
| Historical Pipeline |    ✅   |
| Inference Pipeline  |    ✅   |
| FastAPI             |    ✅   |
| Docker              |   🚧   |

---

# Objetivo

Predecir el resultado de un partido de fútbol como un problema de clasificación multiclase.

Clases:

* HOME
* DRAW
* AWAY

El modelo utiliza exclusivamente información disponible antes del inicio del partido para evitar **data leakage** y garantizar consistencia entre entrenamiento e inferencia.

---

# Arquitectura

El proyecto se divide en dos grandes pipelines independientes.

```
Historical Data
        │
        ▼
 Feature Engineering
        │
        ▼
 Feature Selection
        │
        ▼
 Model Benchmark
        │
        ▼
 Champion Model
        │
        ├──────────────┐
        │              │
        ▼              ▼
Inference Pipeline    FastAPI
        │              │
        ▼              ▼
 Scoring Dataset   Online Predictions
```

Más información:

* `docs/architecture.md`
* `docs/project_structure.md`
* `docs/pipelines.md`

---

# Estructura del proyecto

```
data/
docs/
models/
notebooks/
src/

Dockerfile
requirements.txt
README.md
```

La descripción completa de la estructura se encuentra en:

`docs/project_structure.md`

---

# Champion Model

Modelo seleccionado:

**Stacking Ensemble**

Características principales:

* Top 30 Features
* Random Forest + Logistic Regression
* Meta-model Logistic Regression

Métricas:

| Métrica         |  Valor |
| --------------- | -----: |
| Accuracy        | 0.5123 |
| F1 Macro        | 0.4915 |
| Precision Macro | 0.4934 |
| Recall Macro    | 0.4934 |

Información completa:

`docs/model_card.md`

---

# Historical Pipeline

Reconstruye completamente el proceso de entrenamiento:

* construcción del dataset
* feature engineering
* selección de variables
* entrenamiento
* benchmark
* exportación del Champion Model

Ejecutar:

```bash
python -m src.pipelines.run_historical_pipeline
```

---

# Inference Pipeline

Construye automáticamente el dataset de inferencia utilizando plantillas actuales y próximos partidos.

Incluye:

* scraping de fixtures
* scraping de plantillas
* construcción de team features
* construcción de player features
* generación del scoring dataset
* predicciones batch

Ejecutar:

```bash
python -m src.pipelines.run_inference_pipeline
```

---

# API

La API fue desarrollada utilizando **FastAPI**.

Documentación automática:

```
http://localhost:8000/docs
```

Endpoints disponibles:

### Información

* GET `/`
* GET `/health`
* GET `/model`

### Exploración

* GET `/competitions`
* GET `/matches`

### Predicciones

* POST `/predict_match`
* POST `/predict_batch_matches`
* POST `/predict_features`
* POST `/predict_batch_features`

---

# Instalación

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno.

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# Ejecutar la API

```bash
uvicorn src.api.main:app --reload
```

Abrir:

```
http://localhost:8000/docs
```

---

# Docker

El proyecto incluye un contenedor Docker para desplegar la API de inferencia.

Construcción:

```bash
docker build -t football-ml-api .
```

Ejecución:

```bash
docker run -p 8000:8000 football-ml-api
```

---

# Documentación

La documentación técnica se encuentra en la carpeta `docs`.

* architecture.md
* model_card.md
* pipelines.md
* project_structure.md

---

# Trabajo futuro

El diseño del proyecto permite extender fácilmente el sistema.

Líneas futuras de desarrollo:

* incorporación de nuevas ligas y continentes
* actualización automática del Champion Model
* simulación de fichajes y cambios de plantilla
* incorporación de métricas avanzadas por jugador
* despliegue en AWS
* monitoreo del modelo
* recalibración periódica

---

# Tecnologías

* Python
* Pandas
* Scikit-Learn
* FastAPI
* Playwright
* BeautifulSoup
* Joblib
* Docker

---

# Licencia

Proyecto desarrollado con fines académicos para la materia **Machine Learning en Producción**.
