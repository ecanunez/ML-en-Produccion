# Estructura del Proyecto

## Organización general

El proyecto está organizado siguiendo una arquitectura modular que separa las distintas etapas del ciclo de vida de un sistema de Machine Learning:

* obtención de datos
* procesamiento
* ingeniería de variables
* entrenamiento
* inferencia
* reportes

La siguiente estructura resume los principales componentes del repositorio.

```text
ML-en-Produccion/

├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── docs/
│
├── models/
│
├── notebooks/
│
├── src/
│   ├── config/
│   ├── data/
│   ├── features/
│   │   ├── engineering/
│   │   └── inference/
│   ├── inference/
│   ├── models/
│   ├── pipelines/
│   ├── reports/
│   ├── scraper/
│   │   ├── historical/
│   │   └── inference/
│   └── scoring/
│
└── README.md
```

---

# Descripción de cada módulo

## data/

Contiene todos los datos utilizados durante el proyecto.

### raw/

Datos obtenidos directamente desde las fuentes originales mediante scraping.

Incluye:

* partidos históricos
* partidos futuros
* plantillas de equipos
* información de jugadores

### interim/

Datasets intermedios generados durante el procesamiento.

Estos archivos sirven como entrada para la construcción de variables y permiten desacoplar las distintas etapas del pipeline.

### processed/

Datasets finales utilizados por el entrenamiento y la inferencia.

Ejemplos:

* training_dataset.parquet
* scoring_dataset.parquet
* predictions.csv

---

## docs/

Documentación técnica del proyecto.

Describe la arquitectura, pipelines, estructura del repositorio y funcionamiento general del sistema.

---

## models/

Contiene los modelos entrenados y las distintas versiones publicadas.

Cada versión del modelo campeón incluye su artefacto serializado y la documentación correspondiente.

---

## notebooks/

Espacio destinado a análisis exploratorios y documentación complementaria.

No forma parte del pipeline de producción.

---

## src/

Código fuente del proyecto.

### config/

Configuración centralizada del sistema.

Incluye parámetros del proyecto, configuración de experimentos, conjuntos de variables y competiciones soportadas.

---

### data/

Construcción y procesamiento de datasets históricos.

Incluye la consolidación de temporadas, generación de `matches.parquet`, construcción del `player_mapping` y creación del dataset de entrenamiento.

---

### scraper/

Obtención automática de información desde Transfermarkt.

Se divide en dos módulos independientes:

* `historical/`: descarga de datos históricos.
* `inference/`: descarga de partidos futuros y plantillas actuales.

---

### features/

Construcción de variables utilizadas por el modelo.

Se organiza en:

* `engineering/`: variables para entrenamiento.
* `inference/`: variables para predicción de partidos futuros.

---

### models/

Entrenamiento, evaluación y exportación del modelo campeón.

Incluye el registro de modelos disponibles, carga del dataset, evaluación y serialización del artefacto final.

---

### scoring/

Construcción del dataset utilizado durante la inferencia.

Integra la información de partidos futuros con las variables agregadas de cada equipo para generar el `scoring_dataset`.

---

### inference/

Carga del modelo campeón y generación de predicciones para nuevos partidos.

Produce tanto la clase predicha como las probabilidades asociadas a cada resultado posible.

---

### pipelines/

Orquestación completa del sistema.

Actualmente existen dos pipelines principales:

* Pipeline histórico
* Pipeline de inferencia

Cada uno ejecuta automáticamente todos los pasos necesarios para completar el proceso correspondiente.

---

### reports/

Reportes técnicos generados durante el desarrollo del modelo.

Incluye documentación sobre:

* ingeniería de variables
* selección de características
* benchmark de modelos
* análisis de errores
* historial de experimentos

---

# Filosofía de la organización

La estructura del proyecto busca mantener una separación clara entre:

* adquisición de datos
* construcción de variables
* entrenamiento
* inferencia
* documentación

Esta organización permite que cada etapa pueda evolucionar de manera independiente y facilita la incorporación de nuevos modelos, nuevas variables o nuevas fuentes de datos sin afectar el resto del sistema.
