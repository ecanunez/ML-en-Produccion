# Pipelines del Proyecto

El proyecto cuenta con dos pipelines principales:

1. Pipeline histórico
2. Pipeline de inferencia

Ambos están definidos en `src/pipelines/` y permiten ejecutar de forma ordenada las etapas necesarias para entrenar el modelo o generar predicciones sobre nuevos partidos.

---

# 1. Pipeline histórico

## Objetivo

El pipeline histórico construye el dataset de entrenamiento a partir de datos históricos, genera las variables del modelo, entrena el modelo configurado y exporta el modelo campeón.

Este pipeline se utiliza cuando se quiere reconstruir el proceso completo de entrenamiento.

---

## Comando de ejecución

```powershell
python -m src.pipelines.run_historical_pipeline
```

---

## Flujo general

```text
Datos históricos crudos
        ↓
Consolidación de partidos
        ↓
Construcción de matches.parquet
        ↓
Player mapping
        ↓
Feature engineering histórico
        ↓
training_dataset.parquet
        ↓
Entrenamiento del modelo
        ↓
Exportación del modelo campeón
```

---

## Pasos ejecutados

El pipeline histórico ejecuta los siguientes módulos:

```text
src.data.consolidacion
src.data.build_matches
src.data.build_player_mapping

src.features.engineering.build_player_match_stats
src.features.engineering.build_team_strength_features
src.features.engineering.build_elo_features
src.features.engineering.build_player_profile_features
src.features.engineering.build_player_balance_features
src.features.engineering.create_new_elo_features
src.features.engineering.create_draw_features
src.features.engineering.create_interaction_features

src.data.build_training_dataset
src.models.train
src.models.export_champion_model
```

---

## Outputs principales

El pipeline histórico genera o actualiza:

```text
data/interim/matches.parquet
data/interim/player_mapping.parquet
data/interim/*_features.parquet
data/processed/training_dataset.parquet
models/champion_model.pkl
```

---

## Modelo exportado

El modelo campeón se exporta como un artefacto serializado:

```text
models/champion_model.pkl
```

Este artefacto incluye:

* modelo entrenado
* nombre del modelo
* feature set utilizado
* lista de features esperadas
* métricas de evaluación
* versión del modelo
* timestamp del dataset
* random state

---

# 2. Pipeline de inferencia

## Objetivo

El pipeline de inferencia genera predicciones para partidos futuros.

Este pipeline utiliza partidos próximos, plantillas actuales de equipos, features agregadas y el modelo campeón exportado previamente.

---

## Comando de ejecución

```powershell
python -m src.pipelines.run_inference_pipeline
```

---

## Flujo general

```text
Partidos futuros
        ↓
Plantillas actuales
        ↓
Features de equipo
        ↓
Features de jugadores
        ↓
scoring_dataset.parquet
        ↓
Modelo campeón
        ↓
Predicciones
```

---

## Pasos ejecutados

El pipeline de inferencia puede ejecutarse en dos modalidades.

---

## 2.1. Pipeline con scraping

Incluye la descarga de partidos futuros y plantillas actuales.

```text
src.scraper.inference.scrape_upcoming_matches
src.scraper.inference.scrape_team_squads
src.features.inference.build_team_features
src.features.inference.build_player_features
src.scoring.build_scoring_dataset
src.inference.predict
```

Esta modalidad depende de la disponibilidad de Transfermarkt y puede fallar por timeouts de red.

---

## 2.2. Pipeline desde datos existentes

Utiliza archivos previamente scrapeados y evita depender de la red.

```text
src.features.inference.build_team_features
src.features.inference.build_player_features
src.scoring.build_scoring_dataset
src.inference.predict
```

Esta modalidad fue utilizada para validar el pipeline de inferencia de punta a punta.

---

## Outputs principales

El pipeline de inferencia genera o actualiza:

```text
data/raw/upcoming_matches/*.csv
data/raw/team_squads/*.csv
data/processed/team_features/*.csv
data/processed/team_player_features/*.csv
data/processed/scoring_dataset.csv
data/processed/scoring_dataset.parquet
data/processed/predictions.csv
```

---

# 3. Dataset de scoring

El dataset de scoring es el equivalente de inferencia del dataset de entrenamiento.

```text
training_dataset.parquet  → entrenamiento
scoring_dataset.parquet   → inferencia
```

El archivo activo se mantiene en:

```text
data/processed/scoring_dataset.parquet
```

Cuando se genera una nueva versión, el archivo anterior se respalda automáticamente en:

```text
data/processed/backups/
```

---

# 4. Predicciones

Las predicciones finales se guardan en:

```text
data/processed/predictions.csv
```

El archivo contiene:

* equipos
* predicción final
* probabilidad de victoria visitante
* probabilidad de empate
* probabilidad de victoria local

Ejemplo de columnas:

```text
home_team
away_team
prediction
prob_away
prob_draw
prob_home
```

---

# 5. Validación de pipelines

Ambos pipelines fueron validados luego de la reorganización del proyecto.

## Pipeline histórico

Estado:

```text
Completado correctamente
```

Resultado:

```text
PIPELINE HISTÓRICO COMPLETADO
```

---

## Pipeline de inferencia

Estado:

```text
Completado correctamente
```

Resultado:

```text
PIPELINE DE INFERENCIA COMPLETADO
```

---

# 6. Consideraciones

## Dependencia del scraping

Los pasos de scraping dependen de Transfermarkt y pueden verse afectados por:

* timeouts
* cambios en el HTML
* restricciones temporales del sitio
* disponibilidad de fixtures

Por este motivo, el pipeline de inferencia puede ejecutarse también desde archivos previamente descargados.

---

## Contrato de features

El modelo campeón define la lista de features esperadas dentro del artefacto exportado.

Durante la construcción del scoring dataset, las features esperadas se recuperan desde:

```python
artifact["features"]
```

Esto evita hardcodear manualmente las variables requeridas por el modelo.

---

## Versionado de datasets

El proyecto mantiene archivos activos para entrenamiento e inferencia:

```text
training_dataset.parquet
scoring_dataset.parquet
```

Cuando corresponde, las versiones anteriores se preservan mediante backups fechados.

Esta estrategia evita nombres ambiguos como `final`, `final_v2` o `final_final`, y permite mantener trazabilidad.
