# Model Card

## Modelo campeón

**Versión:** v1.0

---

# Resumen

El modelo campeón del proyecto corresponde a un **Stacking Ensemble** entrenado para predecir el resultado de partidos de fútbol profesional.

Las posibles clases son:

* HOME
* DRAW
* AWAY

El modelo utiliza información agregada de ambos equipos, variables históricas y características derivadas de las alineaciones para estimar las probabilidades de cada resultado.

---

# Objetivo

Estimar la probabilidad de:

* victoria local
* empate
* victoria visitante

a partir de información disponible antes del inicio del partido.

El modelo está pensado para ser utilizado como motor de inferencia dentro del pipeline desarrollado para este proyecto.

---

# Dataset de entrenamiento

El modelo fue entrenado utilizando partidos oficiales correspondientes a las temporadas:

```text
2022
2023
2024
2025
```

Incluye:

* ligas nacionales
* competiciones internacionales

Los datos fueron obtenidos mediante scraping desde Transfermarkt y posteriormente enriquecidos con información histórica de jugadores y equipos.

---

# Tipo de modelo

```text
StackingClassifier
```

Modelo de ensemble construido sobre múltiples clasificadores base y un meta-modelo encargado de combinar sus predicciones.

La selección de esta arquitectura surgió a partir del benchmark realizado durante la etapa de experimentación.

---

# Variables utilizadas

El modelo utiliza un conjunto de **30 variables** seleccionadas mediante análisis de importancia de variables y validación cruzada.

Las features utilizadas se almacenan dentro del propio artefacto exportado.

Durante la inferencia se recuperan automáticamente mediante:

```python
artifact["features"]
```

Esto garantiza que el pipeline de predicción utilice exactamente las mismas variables con las que el modelo fue entrenado.

---

# Métricas de desempeño

Evaluación sobre el conjunto de test:

| Métrica         |      Valor |
| --------------- | ---------: |
| Accuracy        | **0.5123** |
| F1 Macro        | **0.4915** |
| Precision Macro | **0.4934** |
| Recall Macro    | **0.4934** |

---

# Artefacto exportado

El modelo campeón se distribuye como un único artefacto serializado.

```text
models/champion_model.pkl
```

El archivo contiene:

* modelo entrenado
* feature set
* lista de features
* métricas
* versión
* timestamp del dataset
* configuración del experimento

De esta manera el proceso de inferencia no depende de archivos auxiliares externos.

---

# Pipeline de inferencia

Durante la predicción el flujo es:

```text
Upcoming matches
        ↓
Team features
        ↓
Player features
        ↓
Scoring dataset
        ↓
Champion model
        ↓
Prediction
```

El módulo encargado de realizar las predicciones es:

```text
src/inference/predict.py
```

---

# Salida del modelo

Para cada partido el modelo devuelve:

* clase predicha
* probabilidad de victoria visitante
* probabilidad de empate
* probabilidad de victoria local

Ejemplo:

| Home    | Away          | Prediction |  Away |  Draw |  Home |
| ------- | ------------- | ---------- | ----: | ----: | ----: |
| Arsenal | Coventry City | HOME       | 0.241 | 0.368 | 0.391 |

---

# Supuestos

El modelo asume que:

* las plantillas representan razonablemente a los equipos actuales;
* las variables históricas continúan siendo informativas para partidos futuros;
* la calidad del scraping y del proceso de matching de jugadores es suficiente para construir las variables agregadas.

---

# Limitaciones

Entre las principales limitaciones del modelo se encuentran:

* no incorpora lesiones;
* no considera sanciones;
* no utiliza alineaciones confirmadas;
* no modela transferencias ocurridas después del scraping;
* no incorpora información de cuotas de apuestas;
* no utiliza estadísticas recientes partido a partido;
* las variables ELO utilizadas durante la inferencia se aproximan mediante valores neutrales, por lo que representan una simplificación respecto al entrenamiento.

---

# Casos de uso

El modelo fue diseñado para:

* predicción batch de partidos futuros;
* integración en una API REST;
* simulación de modificaciones en plantillas;
* análisis exploratorio de enfrentamientos.

No fue diseñado para apuestas deportivas ni para la toma automática de decisiones financieras.

---

# Trabajo futuro

Las principales líneas de evolución previstas incluyen:

* actualización dinámica del ELO durante la inferencia;
* incorporación de estadísticas recientes por jugador;
* simulación de transferencias;
* calibración de probabilidades;
* incorporación de nuevas variables contextuales;
* publicación mediante una API de inferencia.

## Expansión del dataset

La versión actual del modelo fue entrenada utilizando las principales ligas europeas y competiciones internacionales correspondientes a las temporadas 2022–2025.

Sin embargo, la arquitectura del proyecto fue diseñada para facilitar la incorporación de nuevas competiciones mediante la configuración centralizada de ligas y el pipeline automatizado de scraping y procesamiento.

Las siguientes etapas del proyecto contemplan la incorporación gradual de nuevas ligas de:

- Sudamérica
- Norteamérica
- Asia
- África

Esta ampliación permitirá entrenar modelos sobre un conjunto de datos más diverso y evaluar el impacto de la regionalización en el desempeño predictivo.