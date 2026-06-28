# Production Considerations

Este documento describe las principales decisiones de diseño adoptadas durante el desarrollo del proyecto para facilitar el despliegue del sistema en un entorno de producción.

---

# Data Leakage

Uno de los principales riesgos en problemas de predicción deportiva consiste en incorporar información que únicamente está disponible después de disputado el partido.

Para evitar este problema, el dataset fue construido utilizando exclusivamente información disponible antes del inicio del encuentro.

Entre las principales medidas adoptadas se encuentran:

* exclusión del resultado del partido durante la construcción de las variables;
* utilización de estadísticas históricas acumuladas;
* cálculo de ELO utilizando únicamente partidos anteriores;
* utilización de información de plantillas disponible antes del encuentro;
* exclusión de cualquier información generada durante el partido.

De esta forma, el modelo nunca observa información futura durante el entrenamiento.

---

# Training–Serving Skew

Otro riesgo frecuente consiste en que las variables utilizadas durante el entrenamiento sean diferentes de las disponibles durante la inferencia.

Para minimizar este problema, el proyecto implementa un único contrato de variables.

El Champion Model almacena junto con el modelo:

* features utilizadas;
* versión del modelo;
* métricas;
* metadatos del entrenamiento.

Durante la inferencia, el sistema recupera automáticamente la lista de variables desde el artefacto serializado.

Esto evita mantener listas de columnas hardcodeadas y garantiza consistencia entre entrenamiento e inferencia.

Además, el pipeline de inferencia genera automáticamente todas las variables necesarias antes de ejecutar las predicciones.

---

# Reproducibilidad

El proyecto fue diseñado para permitir reconstruir completamente el modelo.

El pipeline histórico permite regenerar:

* dataset histórico;
* variables derivadas;
* selección de características;
* entrenamiento;
* exportación del Champion Model.

Asimismo, el pipeline de inferencia reconstruye automáticamente el dataset de scoring utilizando datos actualizados.

---

# Versionado

El proyecto mantiene versionados distintos componentes del sistema.

## Código

El código fuente se encuentra versionado mediante Git.

## Modelos

Cada Champion Model incluye:

* modelo serializado;
* metadata del entrenamiento;
* README;
* versión del modelo.

## Experimentos

Los experimentos realizados durante el desarrollo se registran mediante:

* experiment_log.csv
* model_history.md

permitiendo comparar configuraciones y resultados obtenidos.

---

# Arquitectura

El sistema separa claramente entrenamiento e inferencia.

## Pipeline histórico

Responsable de:

* scraping histórico;
* construcción del dataset;
* entrenamiento;
* selección del modelo campeón.

## Pipeline de inferencia

Responsable de:

* scraping de partidos futuros;
* scraping de plantillas;
* construcción del scoring dataset;
* generación de predicciones.

Esta separación facilita el mantenimiento del sistema y reduce el riesgo de inconsistencias entre ambos procesos.

---

# API

La inferencia se expone mediante una API REST desarrollada con FastAPI.

Actualmente soporta:

* predicción online;
* predicción batch;
* consulta de competiciones disponibles;
* consulta de partidos disponibles;
* recuperación de información del modelo.

La documentación interactiva se genera automáticamente mediante OpenAPI / Swagger.

---

# Docker

La API se encuentra containerizada mediante Docker y fue validada ejecutando el servicio de inferencia dentro de un contenedor Linux utilizando la imagen oficial de Python.

La imagen contiene únicamente los componentes necesarios para la inferencia, manteniendo separado el proceso de entrenamiento del servicio de predicción.

---

# Limitaciones actuales

La versión actual presenta algunas limitaciones conocidas.

* El ELO utilizado durante la inferencia se aproxima mediante valores neutrales.
* Algunas competiciones todavía no publican el fixture completo al momento del scraping.
* La cobertura del matching de jugadores depende de la disponibilidad de información en Transfermarkt.

Estas limitaciones fueron consideradas durante el diseño y representan oportunidades de mejora para versiones futuras.

---

# Trabajo futuro

Las siguientes líneas de trabajo permitirán fortalecer el sistema para un entorno de producción.

* actualización automática del Champion Model;
* monitoreo del rendimiento del modelo;
* detección de data drift;
* despliegue en servicios cloud (AWS);
* integración continua (CI/CD);
* simulación de fichajes y cambios de plantilla.

# Dependencias

El proyecto separa las dependencias necesarias para ejecutar la aplicación de aquellas utilizadas para reproducir la release del Champion Model.

Esto facilita la evolución del sistema sin perder la capacidad de reconstruir versiones anteriores del modelo.
