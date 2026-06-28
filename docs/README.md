## Índice

- [Arquitectura](architecture.md)
- [Estructura del proyecto](project_structure.md)
- [Pipelines](pipelines.md)
- [Model Card](model_card.md)

# ML-en-Produccion

Sistema de Machine Learning para la predicción de resultados de partidos de fútbol profesional utilizando datos históricos, información de plantillas y variables derivadas de jugadores y equipos.

El proyecto cubre el ciclo completo de un sistema de Machine Learning:

- recolección automática de datos;
- construcción del dataset;
- ingeniería de variables;
- entrenamiento de modelos;
- selección del modelo campeón;
- generación de predicciones para partidos futuros.

---

# Objetivo

El objetivo principal es desarrollar un sistema capaz de estimar la probabilidad de:

- victoria local (HOME)
- empate (DRAW)
- victoria visitante (AWAY)

utilizando información disponible antes del comienzo del partido.

La arquitectura fue diseñada para facilitar futuras extensiones, como la incorporación de nuevas ligas, simulación de transferencias y despliegue mediante una API REST.

---

# Estado del proyecto

| Etapa | Estado |
|--------|:------:|
| Data Collection | ✅ |
| Data Processing | ✅ |
| Feature Engineering | ✅ |
| Model Training | ✅ |
| Feature Selection | ✅ |
| Ensemble Models | ✅ |
| Champion Model Export | ✅ |
| Historical Pipeline | ✅ |
| Inference Pipeline | ✅ |
| API Deployment | ⏳ |

Versión actual:

```text
v1.0
```

---

# Modelo campeón

El modelo actualmente seleccionado es un **Stacking Ensemble**, entrenado utilizando las treinta variables con mayor capacidad predictiva obtenidas durante la etapa de selección de características.

Métricas obtenidas sobre el conjunto de test:

| Métrica | Valor |
|----------|------:|
| Accuracy | 0.5123 |
| F1 Macro | 0.4915 |
| Precision Macro | 0.4934 |
| Recall Macro | 0.4934 |

---

# Arquitectura

El proyecto se organiza en dos pipelines independientes.

## Pipeline histórico

```text
Scrapers
      ↓
Raw data
      ↓
Matches
      ↓
Player Mapping
      ↓
Feature Engineering
      ↓
Training Dataset
      ↓
Model Training
      ↓
Champion Model
```

---

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

# Documentación

La documentación del proyecto se encuentra organizada en los siguientes documentos.

| Documento | Descripción |
|------------|-------------|
| architecture.md | Arquitectura general del sistema |
| project_structure.md | Organización del repositorio |
| pipelines.md | Descripción de los pipelines históricos e inferencia |
| model_card.md | Documentación del modelo campeón |

Los reportes técnicos generados durante el desarrollo pueden consultarse en:

```text
src/reports/
```

---

# Organización del repositorio

```text
ML-en-Produccion/

data/
docs/
models/
notebooks/
src/
README.md
```

Una descripción detallada de cada módulo se encuentra en:

```text
docs/project_structure.md
```

---

# Componentes principales

El código fuente está organizado en módulos independientes.

```text
src/

config/
data/
scraper/
features/
models/
scoring/
inference/
pipelines/
reports/
```

Cada módulo tiene una única responsabilidad, facilitando el mantenimiento y la evolución del proyecto.

---

# Entrenamiento

Para reconstruir completamente el modelo desde los datos históricos:

```bash
python -m src.pipelines.run_historical_pipeline
```

Este proceso:

- reconstruye el dataset histórico;
- genera todas las variables;
- construye el dataset de entrenamiento;
- entrena el modelo;
- exporta el modelo campeón.

---

# Inferencia

Para generar predicciones sobre nuevos partidos:

```bash
python -m src.pipelines.run_inference_pipeline
```

El pipeline realiza automáticamente:

- descarga de partidos futuros;
- descarga de plantillas;
- construcción del scoring dataset;
- generación de predicciones.

---

# Resultados

El pipeline de inferencia produce principalmente:

```text
data/processed/

scoring_dataset.parquet
predictions.csv
```

Cada predicción incluye:

- equipo local;
- equipo visitante;
- resultado predicho;
- probabilidad de victoria visitante;
- probabilidad de empate;
- probabilidad de victoria local.

---

# Trabajo futuro

Las siguientes líneas de trabajo forman parte de la evolución prevista del proyecto.

## Datos

- incorporación de nuevas ligas nacionales;
- ampliación de competiciones internacionales;
- actualización automática de plantillas.

## Variables

- ELO dinámico para inferencia;
- estadísticas recientes por jugador;
- lesiones y suspensiones;
- historial de enfrentamientos;
- variables contextuales.

## Modelado

- calibración de probabilidades;
- comparación con nuevos algoritmos;
- optimización automática de hiperparámetros.

## Simulación

La arquitectura fue diseñada para permitir, en futuras versiones:

- simulación de transferencias;
- cambios de alineación;
- evaluación del impacto potencial de fichajes sobre las probabilidades estimadas por el modelo.

## Deployment

- API REST
- Docker
- despliegue en la nube

---

# Licencia

Proyecto desarrollado con fines académicos y de investigación.