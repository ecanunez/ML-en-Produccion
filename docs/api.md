# API REST

La API del proyecto permite consultar partidos disponibles y generar predicciones online y batch utilizando el Champion Model exportado.

La API fue desarrollada con **FastAPI** y expone documentación automática mediante Swagger/OpenAPI.

---

# Ejecución

Para levantar la API localmente:

```bash
uvicorn src.api.main:app --reload
```

Luego abrir:

```text
http://localhost:8000/docs
```

---

# Endpoints disponibles

## Información general

| Método | Endpoint  | Descripción                    |
| ------ | --------- | ------------------------------ |
| GET    | `/`       | Estado general del servicio    |
| GET    | `/health` | Health check del servicio      |
| GET    | `/model`  | Información del Champion Model |

---

## Exploración de partidos

| Método | Endpoint                              | Descripción                                         |
| ------ | ------------------------------------- | --------------------------------------------------- |
| GET    | `/competitions`                       | Lista las competiciones disponibles para inferencia |
| GET    | `/matches`                            | Lista los partidos disponibles                      |
| GET    | `/matches?competition=Premier League` | Filtra partidos por competición                     |

---

## Predicciones sobre partidos reales

| Método | Endpoint                 | Descripción                            |
| ------ | ------------------------ | -------------------------------------- |
| POST   | `/predict_match`         | Predicción online de un partido        |
| POST   | `/predict_batch_matches` | Predicción batch de múltiples partidos |

---

## Predicciones mediante features

| Método | Endpoint                  | Descripción                                                 |
| ------ | ------------------------- | ----------------------------------------------------------- |
| POST   | `/predict_features`       | Predicción utilizando directamente las features del modelo  |
| POST   | `/predict_batch_features` | Predicción batch utilizando múltiples conjuntos de features |

---

# Flujo recomendado

La utilización habitual de la API sigue el siguiente flujo.

```text
GET /competitions
        │
        ▼
Seleccionar competición
        │
        ▼
GET /matches
        │
        ▼
Seleccionar partido
        │
        ▼
POST /predict_match
        │
        ▼
Predicción + Probabilidades
```

Este flujo permite consultar únicamente competiciones y partidos realmente disponibles para inferencia.

---

# Información del modelo

El endpoint:

```text
GET /model
```

permite consultar el Champion Model actualmente cargado.

La respuesta incluye:

* versión del modelo;
* nombre del modelo;
* feature set;
* cantidad de variables;
* métricas obtenidas durante la evaluación.

---

# Predicción online

Para obtener la predicción de un partido:

```http
POST /predict_match
```

Request:

```json
{
  "match_id": 0
}
```

Respuesta:

```json
{
  "match_id": 0,
  "home_team": "Arsenal",
  "away_team": "Coventry City",
  "competition": "Premier League",
  "prediction": "HOME",
  "prob_away": 0.2409,
  "prob_draw": 0.3682,
  "prob_home": 0.3908
}
```

---

# Predicción batch

Para múltiples partidos:

```http
POST /predict_batch_matches
```

Request:

```json
{
  "match_ids": [0,1,2,3]
}
```

La respuesta devuelve una lista de predicciones, una por cada partido solicitado.

---

# Predicción mediante features

La API también permite realizar inferencias enviando directamente las variables utilizadas por el modelo.

```http
POST /predict_features
```

Este endpoint está pensado para:

* integración con otros sistemas;
* testing;
* validación del modelo;
* simulaciones.

Las features deben respetar exactamente el contrato definido por el Champion Model.

---

# Predicción batch mediante features

```http
POST /predict_batch_features
```

Permite enviar múltiples registros utilizando la misma estructura del endpoint anterior.

Resulta útil para:

* scoring masivo;
* integración con pipelines externos;
* simulaciones.

---

# Validación

La API utiliza **Pydantic** para validar automáticamente:

* estructura de los requests;
* tipos de datos;
* campos requeridos.

Si el request no cumple el contrato esperado, FastAPI devuelve automáticamente un error HTTP 400 o 422 según corresponda.

---

# Documentación automática

FastAPI genera automáticamente la especificación OpenAPI.

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

---

# Artefactos utilizados

La API consume dos artefactos principales.

```text
models/
    champion_model.pkl

data/processed/
    scoring_dataset.parquet
```

El Champion Model almacena internamente:

* modelo entrenado;
* lista de features;
* versión;
* métricas;
* metadatos.

La API recupera automáticamente esta información durante la inicialización, evitando mantener configuraciones duplicadas.

---

# Consideraciones de diseño

La API fue diseñada para minimizar el riesgo de **training-serving skew**.

Para ello:

* las features esperadas son recuperadas desde el propio artefacto del modelo;
* el pipeline de inferencia genera exactamente las mismas variables utilizadas durante el entrenamiento;
* el `scoring_dataset` constituye el contrato entre entrenamiento e inferencia.

---

# Estado actual

| Funcionalidad           | Estado |
| ----------------------- | :----: |
| Online Prediction       |    ✅   |
| Batch Prediction        |    ✅   |
| Predicción por Features |    ✅   |
| Batch por Features      |    ✅   |
| Swagger UI              |    ✅   |
| OpenAPI                 |    ✅   |
| Validación con Pydantic |    ✅   |

---

# Trabajo futuro

La API fue diseñada para facilitar futuras extensiones.

Entre ellas:

* autenticación y autorización;
* selección de fecha de competición;
* selección automática de la próxima jornada;
* despliegue mediante Docker;
* despliegue en AWS;
* monitoreo y observabilidad;
* versionado de modelos mediante múltiples endpoints.
