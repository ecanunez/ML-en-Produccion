# Obligatorio — Machine Learning en Producción — Curso 2026

## Posgrado de Big Data e Inteligencia Artificial — Universidad ORT Uruguay

---

**Fecha de entrega:** 15/07/26 por el sistema de Gestión.
---

### Integrantes

 * Agustina Nuñez Pomatta - 315124

# Informe Técnico

## 1. Introducción

El objetivo de este proyecto es desarrollar un sistema de Machine Learning capaz de predecir el resultado de partidos de fútbol profesional utilizando información disponible antes del inicio de cada encuentro. El problema se aborda como una tarea de clasificación multiclase, donde el modelo debe estimar si el resultado final será una victoria del equipo local (HOME), un empate (DRAW) o una victoria del equipo visitante (AWAY).

A diferencia de problemas de clasificación tradicionales sobre datasets públicos ya preparados, este proyecto abarca el ciclo completo de desarrollo de un sistema de Machine Learning orientado a producción. Esto incluye la obtención automática de los datos mediante técnicas de web scraping, la construcción del dataset de entrenamiento, el análisis exploratorio de los datos, la ingeniería y selección de variables, el entrenamiento y evaluación de múltiples modelos, la exportación del modelo seleccionado y su integración dentro de una API REST para realizar predicciones tanto online como batch.

La principal fuente de información utilizada fue el sitio Transfermarkt, del cual se extrajeron datos históricos de partidos, plantillas de jugadores y valores de mercado de futbolistas pertenecientes a distintas ligas nacionales e internacionales. A partir de esta información se construyó un conjunto de variables que representan tanto la fortaleza de los equipos como las características de sus planteles, incorporando además métricas derivadas como diferencias de valor de mercado, ratings ELO, estadísticas recientes y variables de interacción.

Durante el desarrollo también se prestó especial atención a aspectos propios de sistemas de Machine Learning en producción, tales como la prevención de data leakage, la consistencia entre entrenamiento e inferencia (training-serving skew), la reproducibilidad de los experimentos, el versionado de modelos y la containerización de la aplicación mediante Docker.

Como resultado, se obtuvo un sistema completo capaz de generar predicciones sobre partidos futuros utilizando un modelo de clasificación entrenado sobre datos históricos y desplegado mediante una API REST documentada con FastAPI y OpenAPI. La arquitectura desarrollada permite además incorporar nuevas competiciones, extender las variables utilizadas y evolucionar el sistema hacia escenarios de despliegue en la nube o simulación de cambios en las plantillas de jugadores.

## 2. Objetivos

### 2.1 Objetivo general

Desarrollar un sistema de Machine Learning capaz de predecir el resultado de partidos de fútbol profesional a partir de información disponible antes del inicio de cada encuentro, implementando un flujo completo de desarrollo que abarque la obtención de datos, construcción del dataset, entrenamiento y optimización del modelo, y su posterior despliegue mediante una API REST preparada para escenarios de inferencia online y batch.

### 2.2 Objetivos específicos

Para alcanzar este objetivo general se plantearon los siguientes objetivos específicos:

* Diseñar e implementar un proceso automatizado de recolección de datos mediante técnicas de web scraping sobre fuentes públicas de información futbolística.

* Construir un dataset histórico integrando información de partidos, jugadores y equipos, garantizando la consistencia y calidad de los datos utilizados para el entrenamiento.

* Realizar un análisis exploratorio de los datos (EDA) con el fin de comprender la distribución del problema, detectar posibles inconsistencias y orientar el proceso de ingeniería de variables.

* Desarrollar variables derivadas que representen la fortaleza de los equipos, el rendimiento reciente y las características de sus plantillas, incorporando tanto información histórica como métricas construidas específicamente para este proyecto.

* Evaluar diferentes algoritmos de clasificación y técnicas de optimización, incluyendo selección de características, ajuste de hiperparámetros y modelos de ensamble, con el objetivo de seleccionar el modelo con mejor capacidad predictiva.

* Implementar mecanismos que favorezcan la reproducibilidad del sistema y contemplen aspectos relevantes para su utilización en producción, como el versionado de modelos, la prevención de data leakage y la consistencia entre entrenamiento e inferencia.

* Exponer el modelo seleccionado mediante una API REST documentada que permita realizar predicciones individuales y por lotes, facilitando su integración con aplicaciones externas.

* Containerizar la aplicación utilizando Docker para garantizar la portabilidad y simplificar su despliegue en diferentes entornos de ejecución.

## 3. Representación del problema

El objetivo inicial del proyecto consistía en desarrollar un sistema capaz de predecir el resultado del mundial de FIFA 2026 en base a los planteles de las distintas selecciones que lo juegan. Sin embargo, dado que este tipo de competencias se dan de manera menos frecuente que otro tipo de compentencias y por tanto se entendió que la construcción de un conjunto de entrenamiento suficientemente representativo resultaba compleja. Por lo que, durante la etapa de diseño se optó por limitar la predicción al resultado de partidos de fútbol profesional.

Asimismo, para la versión inicial del sistema, se optó por restringir la predicción por región geográfica e incorporar datos de las principales ligas europeas, si bien se prevé la expansión futura del sistema.

Una vez acotado el alcance a las principales ligas de futbol profesional, se observó que esta formulación resultaba excesivamente amplia, ya que el resultado de un encuentro depende de una gran cantidad de factores, muchos de ellos imposibles de conocer antes del inicio del partido o directamente no observables.

Entre estos factores pueden mencionarse lesiones de último momento, decisiones tácticas de los entrenadores, estado físico y anímico de los jugadores, condiciones climáticas, sanciones, rotaciones de plantel e incluso situaciones aleatorias propias del desarrollo del juego. Pretender modelar simultáneamente todas estas variables hubiera requerido fuentes de información adicionales y un nivel de actualización permanente que excedía el alcance del proyecto.

Por este motivo se decidió reformular el problema, restringiéndolo a la información que razonablemente puede conocerse antes del comienzo de un partido y que, al mismo tiempo, puede obtenerse de forma automática y reproducible. 

Esta decisión permitió construir un sistema consistente tanto para entrenamiento como para inferencia, evitando depender, durante el entrenamiento de información disponible únicamente una vez finalizado el encuentro y por lo tanto no disponible para la inferencia.

Bajo esta formulación, el problema se definió como una tarea de clasificación multiclase, donde cada observación representa un partido y la variable objetivo corresponde al resultado final del encuentro, con tres posibles clases:

* **HOME:** victoria del equipo local.
* **DRAW:** empate.
* **AWAY:** victoria del equipo visitante.

Cada partido se representa mediante un conjunto de variables descriptivas calculadas exclusivamente a partir de información previa al encuentro. Estas variables incluyen indicadores de fortaleza histórica de los equipos, diferencias de valor de mercado entre plantillas, métricas derivadas de jugadores, ratings ELO, estadísticas recientes y otras características construidas durante la etapa de ingeniería de variables.

Esta representación presenta una ventaja adicional desde el punto de vista del despliegue. Al depender únicamente de información disponible antes del inicio del partido, el mismo proceso utilizado para construir el conjunto de entrenamiento puede reproducirse posteriormente para generar predicciones sobre partidos futuros. De esta forma se garantiza la coherencia entre entrenamiento e inferencia y se facilita la integración del modelo dentro de un sistema de predicción en producción.

Finalmente, si bien esta formulación simplifica un problema inherentemente complejo, permite capturar una parte significativa de la información relevante previa a cada encuentro y constituye una base sólida sobre la cual incorporar nuevas variables y fuentes de información en futuras versiones del sistema.


## 4. Construcción del Dataset

Una vez definida la representación del problema, el siguiente desafío consistió en obtener un conjunto de datos que permitiera entrenar el modelo bajo las restricciones establecidas en la etapa anterior. En particular, era necesario disponer de información histórica correspondiente al estado de los equipos antes del inicio de cada partido, garantizando además que el mismo proceso pudiera reproducirse posteriormente para realizar predicciones sobre encuentros futuros.

Si bien existen numerosos datasets públicos relacionados con el fútbol profesional, la mayoría de ellos presentan al menos una de las siguientes limitaciones: contienen únicamente resultados históricos, no incorporan información detallada sobre los jugadores, no permiten reconstruir el estado de las plantillas previo a cada encuentro o no pueden actualizarse de manera automática para nuevas temporadas. Estas restricciones dificultaban la construcción de un sistema orientado a producción y limitaban la posibilidad de extender el proyecto en el tiempo.

Por este motivo se decidió construir un dataset propio mediante un proceso automatizado de adquisición de datos. Esta decisión permitió controlar tanto el contenido como la estructura de la información utilizada durante el entrenamiento, garantizando además la posibilidad de reconstruir el dataset completo cuando fuera necesario.

Como fuente principal de información se seleccionó el sitio **Transfermarkt**, debido a que concentra datos históricos de partidos, plantillas de jugadores, valores de mercado, competiciones y estadísticas individuales dentro de una misma plataforma. Esta integración resultó especialmente valiosa, ya que permitió combinar información correspondiente a distintas entidades sin depender de múltiples proveedores de datos.

El proceso de construcción del dataset se diseñó como un pipeline compuesto por varias etapas independientes. En primer lugar, se descargó el historial de partidos de las competiciones seleccionadas. Posteriormente se obtuvieron los datos de los jugadores y sus valores de mercado, construyéndose un proceso de vinculación entre cada partido y los futbolistas que participaron en él. Finalmente, toda esta información se integró en un único dataset histórico sobre el cual se desarrolló la etapa de ingeniería de variables.

La separación del proceso en etapas independientes permitió simplificar el mantenimiento del sistema, facilitar la detección de errores durante la construcción de los datos y favorecer la reutilización de componentes tanto para el entrenamiento del modelo como para el pipeline de inferencia desarrollado posteriormente.

                  Adquisición de datos
                 (proceso independiente)

          Transfermarkt
                 │
                 ▼
             Scrapers
                 │
                 ▼
          Raw Historical Data
                 │
─────────────────┼──────────────────────────
                 │
                 ▼
        Pipeline Histórico

        Raw Data
             │
             ▼
      Construcción Dataset
             ▼
 Feature Engineering
             ▼
 Training Dataset

### 4.1 Adquisición de datos y construcción del dataset

Durante el diseño del sistema se decidió separar el proceso de adquisición de datos del proceso de construcción del dataset de entrenamiento.

La adquisición de datos comprende las tareas de web scraping sobre la fuente de información seleccionada y constituye un proceso costoso tanto en tiempo de ejecución como en dependencia de servicios externos. Por este motivo no forma parte del pipeline histórico utilizado para reconstruir el modelo, sino que se ejecuta de manera independiente únicamente cuando resulta necesario actualizar la información disponible.

Una vez descargados los datos históricos, el pipeline de entrenamiento opera exclusivamente sobre archivos almacenados localmente. Esta decisión permite reducir significativamente los tiempos de ejecución, garantizar la reproducibilidad del proceso y eliminar la dependencia de conexiones de red o posibles modificaciones en la fuente de datos durante la etapa de entrenamiento.

La separación entre adquisición de datos y construcción del dataset constituye además una ventaja desde el punto de vista del mantenimiento, ya que ambos procesos pueden evolucionar de manera independiente sin afectar el resto de la arquitectura del sistema.

## 5. Análisis Exploratorio de Datos (EDA)

El análisis exploratorio de los datos constituyó una etapa transversal al desarrollo del proyecto. Más que una actividad realizada exclusivamente al inicio del entrenamiento, el EDA fue utilizado como una herramienta para comprender el comportamiento del conjunto de datos, validar la calidad de la información recolectada y orientar las decisiones tomadas durante las etapas posteriores de ingeniería de variables y selección del modelo.

En una primera instancia, el análisis se centró en verificar la consistencia del dataset construido. Se evaluó la distribución de la variable objetivo, la presencia de valores faltantes, la existencia de observaciones inconsistentes y la cobertura alcanzada por el proceso de vinculación entre jugadores y partidos (player mapping). Esta etapa permitió asegurar que el conjunto de entrenamiento representara adecuadamente el problema definido y detectar posibles fuentes de error antes de iniciar el entrenamiento de los modelos.

Posteriormente, el análisis exploratorio se utilizó para comprender mejor las relaciones existentes entre las variables construidas. Se estudiaron distribuciones, correlaciones y diferencias entre clases, identificando patrones que posteriormente dieron origen a nuevas variables derivadas y permitieron simplificar otras cuya información resultaba redundante.

Finalmente, el EDA acompañó las etapas de evaluación del modelo mediante el análisis de importancia de variables y el estudio de los errores de clasificación. Estos análisis permitieron comprender cuáles eran las características con mayor capacidad predictiva, identificar las situaciones donde el modelo presentaba mayores dificultades —particularmente en la predicción de empates— y orientar las sucesivas iteraciones de optimización del sistema.

En conjunto, el análisis exploratorio no solo permitió validar la calidad del dataset, sino que se convirtió en una herramienta de apoyo para la toma de decisiones durante todo el ciclo de desarrollo del proyecto.

### 5.1 Validación y calidad del dataset

Antes de iniciar el entrenamiento de los modelos fue necesario verificar que el conjunto de datos construido representara correctamente el problema definido y cumpliera con las condiciones mínimas de calidad requeridas para un proceso de aprendizaje supervisado.

El primer aspecto analizado fue la consistencia del dataset histórico. Se verificó que cada observación correspondiera a un único partido, eliminando registros incompletos o inconsistentes que pudieran afectar el proceso de entrenamiento. Asimismo, se controló la presencia de valores faltantes en las variables críticas y se definieron estrategias de tratamiento para aquellos casos donde la información disponible no permitía reconstruir completamente determinadas características.

Otro aspecto relevante fue la distribución de la variable objetivo. Dado que el problema fue formulado como una clasificación multiclase (HOME, DRAW y AWAY), se analizó el número de observaciones pertenecientes a cada categoría con el objetivo de identificar posibles desbalances que pudieran influir sobre el comportamiento del modelo. Si bien la distribución no resultó perfectamente uniforme —como es esperable en competiciones de fútbol profesional debido a la ventaja deportiva del equipo local—, las tres clases presentaron una cantidad suficiente de ejemplos para permitir el entrenamiento del clasificador sin necesidad de aplicar técnicas adicionales de balance del dataset.

También se evaluó la calidad del proceso de asociación entre partidos y jugadores (player mapping), etapa fundamental para la posterior construcción de variables derivadas de las características de los planteles. Este análisis permitió cuantificar la cobertura alcanzada por el procedimiento de vinculación y detectar aquellos encuentros en los que no fue posible identificar la totalidad de los futbolistas participantes. En lugar de descartar sistemáticamente estos registros, se optó por diseñar las variables de manera que pudieran aprovechar la información disponible, preservando la mayor cantidad posible de observaciones para el entrenamiento.

En conjunto, estas verificaciones permitieron confirmar que el dataset presentaba un nivel adecuado de calidad y consistencia para avanzar hacia las siguientes etapas del proyecto, proporcionando además una comprensión más profunda de sus fortalezas y limitaciones antes de iniciar el proceso de ingeniería de variables.

┌────────────────────────────────────────────┐
│        VALIDACIÓN DEL DATASET              │
├────────────────────────────────────────────┤
│ Partidos históricos           12.599       │
│ Clases                        3            │
│ Observaciones eliminadas       4           │
│ Missing críticos               0           │
│ Cobertura Player Mapping      6.8 / 11     │
│ Distribución target      44 / 25 / 31 %    │
└────────────────────────────────────────────┘

### 5.2 Comprensión de las variables

Una vez validada la calidad del dataset, el siguiente paso consistió en comprender el comportamiento de las variables disponibles y analizar qué información aportaban respecto al problema de clasificación planteado. El objetivo de esta etapa no fue únicamente describir el conjunto de datos, sino identificar patrones que permitieran representar de manera más adecuada la fortaleza relativa de los equipos antes del inicio de cada partido.

El análisis exploratorio evidenció que ninguna variable individual resultaba suficiente para explicar el resultado de un encuentro. Si bien algunas características mostraban una mayor capacidad descriptiva —como el valor de mercado de los planteles o el rendimiento reciente de los equipos—, el comportamiento observado sugería que el resultado de un partido depende de la interacción entre múltiples factores deportivos.

A partir de este análisis también se identificaron grupos de variables altamente correlacionadas. En varios casos, diferentes indicadores describían esencialmente la misma información desde perspectivas distintas, lo que permitió detectar oportunidades para simplificar la representación del problema sin perder capacidad descriptiva. Estas observaciones resultarían posteriormente relevantes durante la etapa de selección de características.

Otro aspecto de interés surgió al analizar las diferencias entre partidos equilibrados y partidos con una clara diferencia de nivel entre ambos equipos. Se observó que variables asociadas a la fortaleza relativa de los planteles, como las diferencias de valor de mercado o los ratings ELO, presentaban comportamientos consistentes con la intuición deportiva y constituían buenos candidatos para la construcción de nuevas variables derivadas.

Finalmente, el análisis permitió confirmar que la combinación de información proveniente de distintas fuentes ofrecía una representación significativamente más rica del problema que la utilización aislada de estadísticas de equipos o jugadores. Esta conclusión motivó el desarrollo de una etapa específica de ingeniería de variables destinada a integrar dichas fuentes de información en nuevas características con mayor capacidad predictiva.

             INFORMACIÓN DISPONIBLE

          Equipos        Jugadores

             │               │
             ▼               ▼

      Rendimiento      Valor de mercado
      reciente         Edad
      ELO              Experiencia
      ...              ...

             └──────┬────────┘
                    ▼

      Representación del partido


### 5.3 EDA orientado al modelo

El análisis exploratorio de los datos no concluyó una vez iniciado el entrenamiento de los modelos. Por el contrario, los resultados obtenidos durante las primeras iteraciones permitieron formular nuevas preguntas sobre el comportamiento del sistema, convirtiendo al EDA en una herramienta de mejora continua a lo largo del proyecto.

Una vez entrenados los primeros modelos, se analizaron tanto las variables con mayor capacidad predictiva como los principales errores de clasificación. Este proceso permitió comprender qué características aportaban realmente información útil al modelo y cuáles resultaban redundantes o presentaban una contribución marginal. Como consecuencia, el análisis exploratorio dejó de centrarse únicamente en los datos y pasó a incorporar también el comportamiento del propio modelo.

En esta etapa se utilizaron distintas técnicas de interpretabilidad, entre ellas el análisis de importancia de variables y la evaluación mediante Permutation Importance. Estas herramientas permitieron identificar las características con mayor influencia sobre las predicciones, validar hipótesis surgidas durante la etapa de ingeniería de variables y orientar el proceso posterior de selección de características.

De forma complementaria, se realizó un análisis específico de los errores de clasificación, prestando especial atención a aquellos partidos cuya predicción resultaba sistemáticamente más compleja. Este estudio puso de manifiesto que los encuentros con resultados de empate presentaban una mayor dificultad para todos los modelos evaluados, comportamiento consistente con la naturaleza del problema y con la menor separabilidad existente entre equipos de fortaleza similar.

En conjunto, estos análisis permitieron comprender mejor tanto el comportamiento del dataset como el del modelo entrenado, proporcionando evidencia objetiva para las decisiones adoptadas durante las etapas posteriores de optimización y selección del modelo campeón.


## 6. Ingeniería de Variables

El análisis exploratorio permitió comprender que las variables originales disponibles no resultaban suficientes para representar adecuadamente la complejidad del problema planteado. Si bien el dataset reunía información valiosa sobre equipos, jugadores y competiciones, gran parte de dicha información se encontraba dispersa entre distintas fuentes o describía únicamente características individuales de cada entidad.

Con el objetivo de proporcionar al modelo una representación más informativa del estado relativo de ambos equipos antes del inicio de cada partido, se desarrolló una etapa específica de ingeniería de variables. En lugar de limitarse a incorporar nuevas características, esta etapa buscó transformar la información disponible en indicadores capaces de reflejar conceptos deportivos que no podían observarse directamente en los datos originales.

Entre estos conceptos se encuentran la fortaleza histórica de los equipos, el rendimiento reciente, la calidad y equilibrio de las plantillas, la experiencia internacional de los jugadores y la diferencia relativa entre ambos contendientes. La construcción de estas variables permitió expresar de manera cuantitativa aspectos que habitualmente forman parte del análisis deportivo realizado por entrenadores, periodistas y aficionados, facilitando que el modelo pudiera incorporarlos durante el proceso de aprendizaje.

El proceso de ingeniería de variables constituyó una de las etapas más importantes del proyecto, ya que permitió integrar información procedente de distintas fuentes y niveles de agregación en una representación homogénea de cada partido. Como resultado, el modelo dejó de trabajar únicamente con estadísticas aisladas para utilizar una descripción más completa de la situación previa a cada encuentro.

Con el propósito de facilitar el análisis y mantenimiento del sistema, las variables desarrolladas se organizaron en diferentes familias según el tipo de información que representan. En las siguientes secciones se describen los principales grupos de características incorporados y la motivación que justificó su construcción.

### 6.1 Variables de fortaleza de equipos

Uno de los primeros desafíos identificados durante la etapa de ingeniería de variables fue encontrar una forma de representar la fortaleza deportiva de cada equipo antes del inicio de un partido. Si bien el dataset original contenía información sobre los encuentros disputados y las características de los jugadores, no existía un indicador que resumiera el nivel competitivo alcanzado por cada equipo a lo largo del tiempo.

Para abordar este problema se decidió combinar distintas perspectivas de análisis. Por un lado, se incorporaron variables asociadas al rendimiento reciente de los equipos, considerando indicadores como los resultados obtenidos en los últimos encuentros, la cantidad de puntos acumulados, la diferencia de goles y otras métricas capaces de reflejar el estado de forma previo a cada partido. Estas variables permiten representar la evolución temporal del rendimiento, capturando situaciones que una estadística histórica agregada no logra reflejar.

Sin embargo, el rendimiento reciente por sí solo no resulta suficiente para caracterizar la fortaleza relativa de un equipo. Dos equipos pueden llegar con resultados similares enfrentando rivales de niveles muy diferentes. Por este motivo se incorporó además un sistema de calificación basado en ratings ELO, ampliamente utilizado para estimar la fuerza relativa de competidores en distintos ámbitos deportivos.

La utilización del rating ELO permitió representar de manera dinámica la evolución histórica de cada equipo a lo largo de las temporadas analizadas. A diferencia de otras métricas acumulativas, este enfoque considera simultáneamente el historial de resultados y la calidad de los rivales enfrentados, proporcionando una estimación más estable de la fortaleza competitiva de cada equipo.

Finalmente, más que utilizar los valores absolutos de estas variables, el análisis exploratorio mostró que resultaba más informativo representar las diferencias existentes entre ambos equipos. En consecuencia, se construyeron indicadores capaces de describir la ventaja relativa del equipo local respecto al visitante, proporcionando al modelo una representación más cercana al proceso de comparación que naturalmente realiza una persona al analizar un partido de fútbol.

En conjunto, estas variables constituyen la primera aproximación a la descripción del contexto deportivo de cada encuentro y sirven como base para integrar posteriormente la información proveniente de las características individuales de los jugadores.

                 Fortaleza del equipo

              ┌──────────────────────┐
              │                      │
              ▼                      ▼
      Rendimiento reciente      Rating ELO
              │                      │
              └──────────┬───────────┘
                         ▼
            Fortaleza relativa del equipo

### 6.2 Variables derivadas de los jugadores

La fortaleza de un equipo no depende únicamente de sus resultados recientes o de su desempeño histórico. En gran medida, también está determinada por las características de los jugadores que integran el plantel disponible para disputar cada encuentro. Por este motivo, una parte importante de la ingeniería de variables se orientó a construir indicadores capaces de resumir la composición y calidad de los equipos a partir de la información individual de sus futbolistas.

Sin embargo, representar directamente a cada jugador como una variable independiente hubiera generado un espacio de características excesivamente grande y poco generalizable. Además, este enfoque habría dificultado la aplicación del modelo a nuevos partidos y futuros mercados de pases, donde la identidad de los jugadores cambia constantemente.

Como alternativa, se decidió describir cada plantilla mediante variables agregadas capaces de representar propiedades colectivas del equipo. Entre ellas se incluyeron indicadores asociados al valor de mercado, la edad promedio, la experiencia internacional, la cantidad de partidos disputados con la selección nacional y otras métricas construidas a partir de la información individual disponible para cada futbolista.

Una decisión adicional consistió en agrupar estas características según la posición natural de los jugadores dentro del campo de juego. De esta forma fue posible construir descripciones independientes para arqueros, defensores, mediocampistas y delanteros, permitiendo al modelo capturar diferencias que podrían quedar ocultas al considerar únicamente indicadores globales del plantel. Por ejemplo, dos equipos con un valor de mercado similar pueden presentar distribuciones muy diferentes de dicho valor entre sus líneas defensivas y ofensivas.

El resultado de este proceso fue una representación compacta del plantel de cada equipo, capaz de sintetizar información proveniente de decenas de jugadores mediante un conjunto reducido de variables con significado deportivo. Estas características complementan las variables de fortaleza de equipos descritas anteriormente y permiten incorporar al modelo una visión más detallada de la calidad y composición de las plantillas participantes.

### 6.3 Variables comparativas

Las variables construidas hasta este punto permitían describir de manera independiente tanto la fortaleza histórica de los equipos como las características de sus respectivos planteles. Sin embargo, durante el análisis exploratorio surgió una observación importante: el resultado de un partido no depende únicamente del nivel absoluto de cada equipo, sino de la diferencia existente entre ambos.

En efecto, conocer el valor de mercado de un equipo o su rating ELO aporta información relevante, pero resulta aún más útil comprender cuál es la ventaja relativa que presenta respecto a su rival. Dos equipos con un elevado valor de mercado pueden protagonizar un encuentro muy equilibrado, mientras que un equipo de menor valor puede ser ampliamente favorito si enfrenta a un rival considerablemente más débil.

Por este motivo se incorporó una familia de variables comparativas cuyo objetivo consiste en describir explícitamente la relación entre ambos equipos antes del inicio del partido. Estas variables representan diferencias entre indicadores equivalentes de los equipos local y visitante, permitiendo al modelo identificar de forma directa cuál de ellos presenta una ventaja relativa en aspectos como experiencia, rendimiento reciente, fortaleza histórica o calidad de la plantilla.

Además de las diferencias simples, en algunos casos también se construyeron medidas basadas en el valor absoluto de dichas diferencias. Este tipo de representación permite distinguir entre partidos equilibrados y encuentros donde existe una marcada diferencia de nivel entre ambos equipos, independientemente de cuál de ellos actúe como local o visitante.

La incorporación de variables comparativas constituyó un cambio importante en la representación del problema, ya que el modelo dejó de analizar únicamente las características individuales de cada equipo para centrarse también en la relación existente entre ambos. Esta forma de representar un partido resulta más cercana al razonamiento utilizado habitualmente por las personas al realizar un pronóstico deportivo, donde la comparación entre los contendientes suele ser más relevante que sus características consideradas de manera aislada.

### 6.4 Variables de interacción

Las variables desarrolladas en las secciones anteriores permitieron describir distintos aspectos de los equipos participantes desde perspectivas complementarias. Sin embargo, durante el análisis exploratorio se observó que algunos conceptos deportivos no podían representarse adecuadamente mediante una única variable, sino que surgían de la combinación de varias de ellas.

Por ejemplo, la fortaleza histórica de un equipo adquiere un significado diferente cuando se interpreta junto con la calidad de su plantilla. De manera similar, la experiencia internacional de los jugadores puede resultar más relevante cuando se analiza en conjunto con el rendimiento reciente del equipo o con la diferencia existente respecto al rival. Estas situaciones reflejan relaciones que difícilmente pueden capturarse considerando cada característica de forma aislada.

Con el objetivo de representar este tipo de información se incorporó un conjunto de variables de interacción, construidas a partir de la combinación de indicadores previamente desarrollados. Estas nuevas variables buscan expresar relaciones entre distintos aspectos del juego, integrando información procedente de múltiples fuentes en una única representación.

La incorporación de variables de interacción permitió enriquecer la descripción de cada partido sin necesidad de incorporar nuevas fuentes de datos. En lugar de aumentar la cantidad de información disponible, esta estrategia aprovechó de forma más eficiente las características ya construidas, generando representaciones capaces de reflejar patrones más complejos del contexto previo a cada encuentro.

Si bien no todas las variables de interacción aportaron la misma utilidad durante el entrenamiento, su incorporación permitió explorar nuevas formas de representar el problema y contribuyó al proceso posterior de selección de características, donde únicamente se conservaron aquellas que demostraron aportar información relevante para el modelo final.


### 6.5 Representación final del partido

El proceso de ingeniería de variables permitió transformar un conjunto heterogéneo de datos históricos en una representación estructurada del contexto previo a cada encuentro. A partir de información procedente de equipos, jugadores, resultados históricos y características de las competiciones, fue posible construir una descripción integrada de cada partido utilizando únicamente información disponible antes de su inicio.

Más que incrementar la cantidad de variables disponibles, el objetivo de esta etapa consistió en mejorar la calidad de la representación utilizada por el modelo. Cada nueva característica incorporada buscó capturar un aspecto específico del problema, mientras que las variables comparativas y de interacción permitieron expresar relaciones que no resultaban evidentes en los datos originales.

Como resultado, cada partido dejó de estar representado únicamente por información descriptiva de los equipos participantes para convertirse en una caracterización multidimensional de su contexto deportivo. Esta representación integra indicadores de fortaleza histórica, rendimiento reciente, composición de las plantillas, diferencias relativas entre ambos equipos y relaciones entre dichas características, proporcionando una visión más completa del escenario previo a cada encuentro.

Si bien el proceso de ingeniería de variables permitió construir una representación significativamente más rica del problema, también incrementó el número de características disponibles para el modelo. Esto planteó un nuevo desafío: determinar cuáles de ellas aportaban realmente información útil para la predicción y cuáles podían eliminarse sin afectar el rendimiento del sistema.

Por este motivo, la siguiente etapa del proyecto estuvo dedicada a la selección de características, con el objetivo de identificar el conjunto de variables que ofreciera el mejor equilibrio entre capacidad predictiva, simplicidad del modelo y facilidad de mantenimiento.

## 7. Selección de Características

La etapa de ingeniería de variables permitió construir una representación considerablemente más rica del problema de clasificación. Sin embargo, el incremento en la cantidad de características disponibles planteó un nuevo desafío: no todas las variables aportan la misma información al proceso de aprendizaje y, en muchos casos, varias de ellas describen conceptos similares desde perspectivas diferentes.

Mantener un conjunto excesivamente extenso de variables puede incrementar la complejidad del modelo, dificultar su interpretación e incluso introducir información redundante que no contribuya a mejorar su capacidad predictiva. Por este motivo se incorporó una etapa específica de selección de características, orientada a identificar el subconjunto de variables que ofreciera el mejor equilibrio entre rendimiento, simplicidad y mantenibilidad del sistema.

Más que buscar la menor cantidad posible de variables, el objetivo consistió en conservar únicamente aquellas que aportaran información relevante para la predicción del resultado del partido. Esta estrategia permitió reducir la complejidad del modelo sin perder la riqueza descriptiva obtenida durante la etapa de ingeniería de variables.

Para evaluar el impacto de la selección de características se realizaron distintos experimentos comparando conjuntos de variables de diferente tamaño. Estos experimentos permitieron analizar cómo evolucionaba el desempeño del modelo a medida que se incorporaban nuevas características y determinar el punto a partir del cual el incremento en la complejidad dejaba de traducirse en mejoras significativas de rendimiento.

Los resultados obtenidos permitieron seleccionar un conjunto reducido de variables con elevada capacidad predictiva, que posteriormente fue utilizado durante el entrenamiento y la evaluación del modelo campeón.

### 7.1 Estrategia de selección

Una vez definido el conjunto de variables construido durante la etapa de ingeniería de características, fue necesario establecer un criterio objetivo para determinar cuáles de ellas debían formar parte del modelo final. En lugar de seleccionar variables únicamente por intuición o conocimiento del dominio, se optó por un proceso experimental basado en evidencia obtenida durante el entrenamiento de los modelos.

Como primer paso se analizaron las contribuciones individuales de las distintas variables, identificando aquellas con mayor capacidad para discriminar entre las clases del problema. Este análisis permitió detectar tanto características altamente informativas como grupos de variables que aportaban información similar, facilitando la identificación de posibles redundancias dentro del conjunto de datos.

Sin embargo, la importancia individual de una variable no resulta suficiente para determinar si debe formar parte del modelo final. En muchos casos, una característica con una contribución aparentemente modesta puede complementar la información proporcionada por otras variables y mejorar el rendimiento global del sistema. Por este motivo, la selección final se basó en el comportamiento del modelo utilizando diferentes subconjuntos de variables y no únicamente en indicadores individuales de importancia.

Con este objetivo se definieron distintos escenarios de evaluación, comparando modelos entrenados con conjuntos de variables de tamaño creciente. Esta estrategia permitió analizar el impacto real que tenía la incorporación de nuevas características sobre las métricas de desempeño y observar el punto a partir del cual el aumento de complejidad dejaba de traducirse en mejoras significativas.

Este enfoque permitió convertir la selección de características en un proceso guiado por evidencia experimental, priorizando aquellas variables que demostraron aportar valor dentro del modelo completo y no solamente de manera aislada. Como resultado, el conjunto final de características representa un equilibrio entre capacidad predictiva, simplicidad e interpretabilidad, manteniendo únicamente la información que contribuye de forma significativa al desempeño del sistema.

### 7.2 Resultados de la selección de características

La estrategia de selección definida en la sección anterior permitió evaluar de forma sistemática el impacto que tenía el número de variables utilizadas sobre el desempeño del modelo. Para ello se construyeron distintos conjuntos de características de tamaño creciente y se entrenó un modelo equivalente sobre cada uno de ellos, comparando posteriormente sus métricas de rendimiento.

Los resultados mostraron que la incorporación de nuevas variables produjo mejoras significativas durante las primeras etapas del proceso. Sin embargo, a medida que aumentaba el número de características disponibles, dichas mejoras comenzaron a disminuir hasta alcanzar un punto donde agregar nuevas variables aportaba beneficios marginales o incluso generaba una ligera degradación del rendimiento.

Este comportamiento confirmó una de las hipótesis planteadas durante el diseño del sistema: una representación más rica del problema no implica necesariamente un mejor modelo. A partir de cierto nivel de complejidad, parte de la información adicional resulta redundante o aporta muy poca capacidad discriminativa, incrementando innecesariamente el tamaño del modelo.

Como consecuencia de estos experimentos se seleccionó un conjunto de treinta variables que ofrecía el mejor equilibrio entre capacidad predictiva y complejidad del sistema. Este subconjunto conservó la mayor parte de la información relevante construida durante la etapa de ingeniería de variables, reduciendo al mismo tiempo la cantidad de características que debían procesarse tanto durante el entrenamiento como en la inferencia.

Además de mejorar la eficiencia del modelo, esta decisión simplificó el mantenimiento del proyecto y redujo el riesgo de incorporar variables redundantes en futuras versiones del sistema. El conjunto seleccionado fue utilizado como base para el entrenamiento del modelo campeón presentado en los capítulos siguientes.

F1 Macro
 ^
 |
 |                         ● Top30
 |                      ●
 |                   ●
 |               ●
 |            ●
 |         ●
 |      ●
 +-------------------------------------->

     Top10   Top20   Top30   Top40

## 8. Entrenamiento y Optimización

Una vez definida la representación del problema y seleccionado el conjunto de variables que ofrecía el mejor equilibrio entre capacidad descriptiva y complejidad, el siguiente paso consistió en identificar el modelo de clasificación más adecuado para resolver el problema planteado.

Más que buscar el algoritmo con la mayor métrica de desempeño, el objetivo de esta etapa fue encontrar una solución que combinara capacidad predictiva, estabilidad y facilidad de despliegue. Dado que el proyecto se concibió como un sistema orientado a producción, la evaluación de los modelos consideró no solamente su rendimiento sobre el conjunto de entrenamiento y validación, sino también aspectos relacionados con su reproducibilidad, mantenibilidad y comportamiento frente a datos no observados.

Con este propósito se desarrolló un proceso iterativo de entrenamiento y evaluación, comparando distintos algoritmos de clasificación, optimizando sus configuraciones y analizando sistemáticamente el impacto de las decisiones adoptadas durante el desarrollo del proyecto. Este proceso permitió seleccionar finalmente un modelo campeón que representa el mejor compromiso entre precisión, robustez y simplicidad para la versión actual del sistema.

### 8.1 Establecimiento de una línea base

Antes de comparar distintos algoritmos de clasificación fue necesario establecer un punto de referencia que permitiera interpretar objetivamente los resultados obtenidos. Sin una línea base, cualquier métrica de desempeño carece de contexto y resulta difícil determinar si un modelo representa realmente una mejora significativa respecto a una solución sencilla.

Con este propósito se definió un modelo de referencia construido deliberadamente con una estrategia simple. El objetivo de este modelo no era obtener el mejor rendimiento posible, sino proporcionar un estándar mínimo de comparación sobre el cual evaluar las distintas alternativas desarrolladas durante el proyecto.

A partir de esta línea base fue posible cuantificar el aporte real de las diferentes etapas del proceso de desarrollo. Cada nueva familia de variables incorporada, cada ajuste realizado sobre los modelos y cada estrategia de optimización implementada fueron evaluados comparando su desempeño respecto a este punto de partida.

Este enfoque permitió medir de forma objetiva la contribución de cada decisión de ingeniería adoptada a lo largo del proyecto. De esta manera, las mejoras observadas en las métricas finales pueden interpretarse como el resultado acumulado de un proceso iterativo de construcción, evaluación y refinamiento, en lugar de atribuirse únicamente a la elección de un algoritmo de clasificación determinado.

La existencia de una línea base también facilitó la identificación de configuraciones que, pese a ser conceptualmente más complejas, no aportaban mejoras relevantes sobre soluciones considerablemente más simples. Esta perspectiva resultó fundamental para orientar el proceso de optimización hacia modelos que ofrecieran un equilibrio adecuado entre rendimiento y complejidad.

### 8.2 Evaluación de alternativas

Una vez establecida la línea base, se evaluaron diferentes enfoques de clasificación con el objetivo de identificar cuáles se adaptaban mejor a las características del problema planteado. Dado que no existía evidencia previa que indicara cuál sería el algoritmo más apropiado para este conjunto de datos, se optó por una estrategia experimental basada en la comparación sistemática de distintas familias de modelos.

Cada alternativa fue entrenada utilizando la misma representación del problema y las mismas condiciones de evaluación, garantizando que las diferencias observadas en las métricas pudieran atribuirse al comportamiento de los modelos y no a variaciones en los datos utilizados durante el entrenamiento.

El proceso de comparación permitió analizar no solamente la capacidad predictiva de cada algoritmo, sino también aspectos relacionados con su estabilidad, sensibilidad a la ingeniería de variables y capacidad para generalizar sobre datos no observados. Esta evaluación puso de manifiesto que distintos modelos presentaban fortalezas y debilidades particulares, lo que confirmó la conveniencia de mantener un enfoque experimental en lugar de asumir de antemano la superioridad de una determinada técnica.

Los resultados obtenidos durante esta etapa también permitieron identificar aquellas familias de modelos con mayor potencial de mejora mediante procesos posteriores de optimización. Como consecuencia, el esfuerzo de ajuste de hiperparámetros y validación se concentró sobre las alternativas que demostraron ofrecer el mejor equilibrio entre rendimiento y robustez.

Este proceso de evaluación sistemática proporcionó la evidencia necesaria para seleccionar un conjunto reducido de modelos candidatos, que posteriormente fueron sometidos a una etapa más exhaustiva de optimización antes de definir el modelo campeón del proyecto.

| Modelo               | Accuracy | F1 Macro |
| -------------------- | -------: | -------: |
| Baseline             |      ... |      ... |
| Logistic Regression  |      ... |      ... |
| Random Forest        |      ... |      ... |
| HistGradientBoosting |      ... |      ... |
| XGBoost              |      ... |      ... |
| LightGBM             |      ... |      ... |
| Stacking Ensemble    |      ... |      ... |


### 8.3 Optimización del modelo

La evaluación comparativa permitió identificar un conjunto reducido de modelos con un desempeño superior al resto de las alternativas analizadas. Sin embargo, esta etapa representó únicamente el punto de partida del proceso de optimización. Una vez seleccionados los modelos más prometedores, el objetivo pasó a ser mejorar su capacidad predictiva sin incrementar innecesariamente la complejidad del sistema.

La optimización se abordó de forma iterativa, evaluando el impacto de diferentes decisiones sobre el rendimiento global del modelo. Entre ellas se incluyeron el ajuste de hiperparámetros, la incorporación progresiva de nuevas familias de variables, la selección del conjunto de características más representativo y la validación sistemática de los resultados obtenidos. Cada modificación fue evaluada de manera independiente, permitiendo determinar objetivamente si aportaba una mejora real al desempeño del sistema.

Durante este proceso también se priorizó la capacidad de generalización del modelo por encima del rendimiento obtenido sobre un único conjunto de entrenamiento. Para ello se utilizaron estrategias de validación que permitieron estimar el comportamiento esperado frente a datos no observados, reduciendo el riesgo de seleccionar configuraciones excesivamente adaptadas a un conjunto particular de partidos históricos.

Uno de los aspectos más relevantes de esta etapa fue comprobar que las mayores mejoras no siempre estuvieron asociadas a modelos más complejos. En varios casos, decisiones relacionadas con la representación del problema y la selección de variables produjeron incrementos de rendimiento comparables —e incluso superiores— a los obtenidos mediante el ajuste de hiperparámetros. Esta observación reforzó una de las principales conclusiones del proyecto: la calidad de la representación del problema resulta tan importante como el algoritmo utilizado para resolverlo.

Como resultado de este proceso iterativo se obtuvo un conjunto reducido de modelos altamente competitivos, que posteriormente fueron evaluados en conjunto para seleccionar la alternativa que ofrecía el mejor equilibrio entre capacidad predictiva, estabilidad y facilidad de despliegue.

### 8.4 Selección del modelo campeón

La etapa final del proceso de entrenamiento consistió en seleccionar el modelo que sería incorporado al pipeline de inferencia y utilizado durante el despliegue del sistema. Esta decisión no se basó únicamente en la obtención de la mayor métrica de desempeño, sino en una evaluación integral que consideró distintos aspectos relacionados con el comportamiento del modelo y su utilización en un entorno de producción.

Entre los criterios considerados se incluyeron la capacidad predictiva medida sobre datos no utilizados durante el entrenamiento, la estabilidad observada durante los procesos de validación, la consistencia de las probabilidades estimadas y la facilidad para integrar el modelo dentro de la arquitectura desarrollada. Este enfoque permitió priorizar soluciones robustas y reproducibles por encima de mejoras marginales obtenidas únicamente sobre un conjunto específico de evaluación.

Como resultado de este proceso se seleccionó un modelo basado en un **Stacking Ensemble**, capaz de combinar las fortalezas de diferentes algoritmos de clasificación en una única predicción. Esta estrategia permitió aprovechar el comportamiento complementario de los modelos individuales, obteniendo un rendimiento superior al alcanzado por cada uno de ellos de forma independiente.

La elección del modelo campeón representa la culminación del proceso iterativo desarrollado a lo largo del proyecto. Su desempeño no puede atribuirse exclusivamente al algoritmo utilizado, sino al conjunto de decisiones adoptadas durante todas las etapas anteriores: la construcción del dataset, la ingeniería de variables, la selección de características y la optimización sistemática de los modelos evaluados.

El modelo seleccionado fue posteriormente exportado junto con toda la información necesaria para garantizar su reproducibilidad, incluyendo la versión utilizada, el conjunto de variables empleado durante el entrenamiento, las métricas obtenidas y los metadatos asociados al proceso de construcción. Esta información constituye la base del pipeline de inferencia y asegura que las predicciones futuras se realicen bajo las mismas condiciones que dieron origen al modelo campeón.

### 8.5 Modelo final

Como resultado del proceso de entrenamiento, evaluación y optimización desarrollado a lo largo del proyecto, se obtuvo un modelo final preparado para integrarse al pipeline de inferencia y ser utilizado durante la generación de predicciones sobre nuevos partidos.

El modelo fue exportado junto con todos los elementos necesarios para garantizar su correcta utilización fuera del entorno de entrenamiento. Además del algoritmo entrenado, se almacenó el conjunto de variables utilizado durante el aprendizaje, la información de versionado, las métricas de evaluación y los metadatos asociados al proceso de construcción. Esta decisión permite asegurar que el modelo pueda reproducirse y utilizarse en distintos entornos manteniendo exactamente las mismas condiciones bajo las cuales fue validado.

La separación entre la etapa de entrenamiento y la etapa de inferencia constituye uno de los principios fundamentales de la arquitectura propuesta. El proceso de aprendizaje se ejecuta únicamente cuando resulta necesario generar una nueva versión del modelo, mientras que el pipeline de inferencia utiliza exclusivamente el modelo previamente exportado para realizar predicciones sobre partidos futuros. Esta estrategia simplifica el despliegue del sistema y reduce significativamente el costo computacional asociado a la operación cotidiana.

El modelo final constituye, por tanto, un artefacto completamente desacoplado del proceso de entrenamiento. Su utilización no requiere reconstruir el dataset histórico ni repetir las etapas de ingeniería de variables desarrolladas durante el aprendizaje, sino únicamente disponer de un conjunto de datos de entrada con la misma estructura utilizada durante el entrenamiento. Esta característica facilita tanto su integración mediante la API REST como su despliegue dentro de un contenedor Docker o en cualquier otro entorno de producción.

De esta forma concluye la etapa de desarrollo del modelo predictivo y comienza la fase orientada a su utilización como componente de un sistema de Machine Learning en producción, cuya arquitectura y mecanismos de despliegue se describen en los capítulos siguientes.

## 9. Arquitectura del Sistema

A medida que el proyecto evolucionó, dejó de consistir únicamente en el entrenamiento de un modelo de clasificación para convertirse en un sistema completo de Machine Learning. Este cambio implicó diseñar una arquitectura capaz de organizar procesos con objetivos muy diferentes, como la adquisición de datos históricos, la construcción del dataset, el entrenamiento del modelo, la generación de predicciones y el consumo del sistema mediante una API.

Desde las primeras etapas del desarrollo se buscó evitar una implementación monolítica donde todas las tareas dependieran de un único script. En su lugar, se optó por una arquitectura modular, organizada en componentes independientes con responsabilidades claramente definidas. Esta decisión facilitó el mantenimiento del proyecto, permitió reutilizar procesos entre distintas etapas del desarrollo y simplificó la incorporación de nuevas funcionalidades sin afectar el resto del sistema.

Uno de los principios más importantes adoptados durante el diseño fue la separación entre los procesos de entrenamiento y los procesos de inferencia. Aunque ambos utilizan parte de la misma infraestructura, responden a necesidades completamente diferentes y poseen ciclos de ejecución independientes. Esta separación permitió optimizar tanto el desarrollo del modelo como su posterior utilización en un entorno de producción.

Las secciones siguientes describen las principales decisiones arquitectónicas adoptadas y la forma en que los distintos componentes interactúan para conformar el sistema completo.

                 Transfermarkt
                       │
               Scrapers independientes
                       │
                Datos históricos
                       │
              Feature Engineering
                       │
               Training Dataset
                       │
                 Model Training
                       │
               Champion Model
                       │
         ┌─────────────┴─────────────┐
         │                           │
   Inference Pipeline           FastAPI
         │                           │
  Predictions.csv              REST API

### 9.1 Separación entre entrenamiento e inferencia

Uno de los principios arquitectónicos más importantes adoptados durante el desarrollo del proyecto fue la separación explícita entre las etapas de entrenamiento e inferencia. Aunque ambas utilizan información proveniente de una misma fuente y comparten parte de la infraestructura desarrollada, responden a objetivos completamente diferentes y poseen ciclos de vida independientes.

El proceso de entrenamiento tiene como finalidad construir una nueva versión del modelo predictivo. Para ello resulta necesario reconstruir el dataset histórico, ejecutar las etapas de ingeniería de variables, entrenar distintos modelos, evaluar su desempeño y seleccionar la mejor alternativa disponible. Estas tareas presentan un elevado costo computacional y solamente necesitan ejecutarse cuando se desea actualizar el modelo incorporando nueva información o modificaciones en la metodología utilizada.

La etapa de inferencia, en cambio, persigue un objetivo completamente distinto. Una vez que el modelo ha sido entrenado y exportado, únicamente es necesario generar la información correspondiente a los nuevos partidos, construir un conjunto de datos con la misma estructura utilizada durante el entrenamiento y aplicar el modelo previamente obtenido para generar las predicciones. Este proceso es considerablemente más liviano y puede ejecutarse cada vez que se desee obtener estimaciones sobre encuentros futuros.

Separar ambos procesos permitió desacoplar el desarrollo del modelo de su utilización cotidiana. Como consecuencia, la generación de predicciones no depende de repetir las etapas de entrenamiento ni de reconstruir el dataset histórico, sino únicamente de disponer del modelo campeón y de los datos necesarios para describir los nuevos partidos. Esta decisión reduce significativamente el tiempo de ejecución del sistema y simplifica su despliegue en distintos entornos.

Esta separación también favorece el mantenimiento y la evolución del proyecto. Las mejoras introducidas en el pipeline de entrenamiento pueden desarrollarse y validarse de forma independiente, mientras que el pipeline de inferencia permanece estable utilizando la última versión aprobada del modelo. De esta manera, el sistema incorpora un flujo de trabajo donde el entrenamiento constituye un proceso ocasional y la inferencia representa la operación cotidiana del sistema.

                 SISTEMA

            ┌───────────────┐
            │ Entrenamiento │
            └───────┬───────┘
                    │
             Champion Model
                    │
                    ▼
            ┌───────────────┐
            │   Inferencia  │
            └───────────────┘
                    │
              Predicciones

### 9.2 Organización modular

A medida que el proyecto fue incorporando nuevas funcionalidades, la complejidad del sistema aumentó considerablemente. Además del entrenamiento del modelo, fue necesario desarrollar procesos de adquisición de datos, construcción del dataset, ingeniería de variables, inferencia, despliegue mediante una API y mecanismos de documentación y versionado. Frente a este escenario, se optó por una organización modular del código fuente basada en la separación de responsabilidades.

Cada módulo fue diseñado para resolver un problema específico dentro del sistema. De esta manera, las tareas relacionadas con la obtención de datos, la construcción de variables, el entrenamiento de modelos, la generación de predicciones y la exposición de servicios mediante la API permanecen desacopladas entre sí, reduciendo las dependencias entre componentes y facilitando el mantenimiento del proyecto.

Esta organización también permitió reutilizar procesos en diferentes etapas del desarrollo. Por ejemplo, las transformaciones utilizadas para construir el dataset histórico pudieron adaptarse posteriormente al pipeline de inferencia, garantizando que las predicciones se realizaran utilizando la misma representación del problema empleada durante el entrenamiento. Del mismo modo, los componentes responsables de la carga del modelo y la generación de predicciones pudieron integrarse tanto en los scripts de inferencia como en la API REST sin necesidad de duplicar código.

Otro beneficio de esta arquitectura modular es la facilidad para incorporar nuevas funcionalidades sin modificar el resto del sistema. La incorporación de nuevos scrapers, nuevas familias de variables o nuevos algoritmos de entrenamiento puede realizarse de manera localizada, minimizando el impacto sobre los componentes ya existentes y favoreciendo la evolución del proyecto a lo largo del tiempo.

Esta estrategia permitió construir una arquitectura flexible y mantenible, donde cada componente posee una responsabilidad claramente definida y puede evolucionar de forma relativamente independiente del resto del sistema. Este enfoque facilita tanto el desarrollo colaborativo como el despliegue del proyecto en un entorno de producción.

### 9.3 Pipelines

La separación entre entrenamiento e inferencia y la organización modular del código dieron origen a dos pipelines principales, cada uno orientado a resolver un problema específico dentro del sistema. Esta decisión permitió estructurar el proyecto en torno a procesos completos de trabajo, en lugar de depender de la ejecución manual de múltiples scripts independientes.

Si bien la obtención de los datos históricos forma parte del flujo general del proyecto, este proceso se mantiene desacoplado del pipeline de entrenamiento. De esta manera, la actualización de la base histórica puede realizarse de manera independiente, mientras que el entrenamiento utiliza siempre una versión consistente y previamente validada del dataset.

El pipeline histórico reúne todas las etapas necesarias para construir una nueva versión del modelo predictivo utilizando la información histórica previamente disponible. Su ejecución comienza con la construcción del dataset de entrenamiento a partir de los datos ya recolectados, continúa con las distintas etapas de ingeniería de variables y finaliza con el entrenamiento, evaluación y exportación del modelo campeón. Debido al costo computacional asociado al entrenamiento, este pipeline solamente necesita ejecutarse cuando se desea generar una nueva versión del modelo.

Por su parte, el pipeline de inferencia utiliza el modelo previamente entrenado para generar predicciones sobre partidos futuros. Este proceso obtiene la información necesaria para describir los nuevos encuentros, construye un dataset con la misma estructura empleada durante el entrenamiento y aplica el modelo campeón para estimar las probabilidades asociadas a cada posible resultado. Al no requerir una nueva etapa de aprendizaje, su ejecución resulta considerablemente más rápida y puede repetirse tantas veces como sea necesario.

La existencia de dos pipelines independientes permite que ambos evolucionen de manera relativamente autónoma. Mejoras en la metodología de entrenamiento no afectan el funcionamiento cotidiano del sistema de inferencia, mientras que modificaciones en la obtención de datos para nuevos partidos pueden incorporarse sin necesidad de reentrenar el modelo existente. Esta separación favorece el mantenimiento del sistema y reduce el riesgo de introducir cambios no deseados en componentes ya validados.

En conjunto, los pipelines constituyen el mecanismo mediante el cual los distintos módulos del proyecto interactúan para ejecutar procesos completos de principio a fin. Esta organización simplifica la utilización del sistema, mejora su mantenibilidad y facilita su evolución hacia futuras versiones sin alterar los componentes ya consolidados

### 9.4 Integración del sistema

Las decisiones arquitectónicas descritas en las secciones anteriores permiten que los distintos componentes del proyecto funcionen de manera coordinada como un único sistema. Si bien cada módulo posee una responsabilidad específica y cada pipeline responde a un objetivo diferente, todos ellos interactúan mediante interfaces bien definidas y utilizando formatos de datos compatibles entre sí.

La integración del sistema se basa en una secuencia de artefactos generados durante las distintas etapas del proceso. Los datos históricos alimentan la construcción del dataset de entrenamiento; este, a su vez, permite generar el modelo campeón, que posteriormente es utilizado por el pipeline de inferencia y por la API REST para producir predicciones sobre nuevos partidos. De esta forma, cada componente consume únicamente la información producida por la etapa anterior, reduciendo el acoplamiento entre módulos y favoreciendo la reutilización de procesos.

Esta organización también facilita la incorporación de nuevas funcionalidades. La actualización del dataset histórico, el desarrollo de nuevas familias de variables, la incorporación de algoritmos alternativos o la evolución de la API pueden realizarse de manera localizada sin requerir modificaciones significativas en el resto del sistema. Como consecuencia, la arquitectura propuesta resulta flexible frente a futuros cambios y permite que el proyecto evolucione de forma incremental.

Desde una perspectiva más amplia, el proyecto se convierte en un sistema integrado, donde cada componente cumple una función específica dentro de un flujo de trabajo común. Esta visión integral constituye uno de los principales resultados del desarrollo realizado y proporciona la base necesaria para las etapas de despliegue y operación descritas en los capítulos siguientes.

                 Transfermarkt
                        │
             (Scraping independiente)
                        │
                        ▼
                Datos históricos
                        │
                        ▼
             Pipeline histórico
                        │
        Dataset + Ingeniería de variables
                        │
                        ▼
               Champion Model
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
     Pipeline de inferencia     API REST
             │                     │
             └──────────┬──────────┘
                        ▼
                  Predicciones


## 10. Consideraciones para Producción

El desarrollo de un modelo con buen desempeño constituye únicamente una parte del desafío que implica construir un sistema de este tipo. Para que dicho modelo pueda utilizarse de forma confiable en un entorno real, resulta necesario considerar una serie de aspectos relacionados con la reproducibilidad, la consistencia de los datos, la mantenibilidad del sistema y la capacidad de evolución de la solución propuesta.

En este proyecto, las decisiones adoptadas durante el diseño de la arquitectura y de los pipelines no estuvieron orientadas exclusivamente a mejorar las métricas predictivas, sino también a facilitar la operación del sistema una vez finalizada la etapa de entrenamiento. Esto implicó prestar especial atención a la separación entre entrenamiento e inferencia, al versionado de los artefactos generados, a la utilización consistente de las variables del modelo y a la construcción de una arquitectura modular que favoreciera futuras ampliaciones.

Las secciones siguientes presentan las principales consideraciones adoptadas para aproximar el proyecto a un escenario de producción, describiendo tanto las decisiones implementadas como las limitaciones que aún permanecen abiertas para futuras versiones del sistema.

### 10.1 Reproducibilidad y versionado

Uno de los principios fundamentales considerados durante el desarrollo del proyecto fue garantizar que el modelo pudiera reproducirse de manera consistente a lo largo del tiempo. Dado que no resulta suficiente conservar únicamente el modelo entrenado; también es necesario preservar toda la información que permita reconstruir las condiciones bajo las cuales dicho modelo fue generado.

Con este objetivo, cada versión del modelo campeón se almacena junto con los metadatos asociados al proceso de entrenamiento, incluyendo la versión del modelo, el conjunto de variables utilizado, las métricas de evaluación obtenidas y la configuración empleada durante su construcción. Esta información permite identificar de manera precisa qué artefacto fue utilizado para generar una determinada predicción y facilita la comparación entre distintas versiones del sistema.

La reproducibilidad también fue considerada durante el diseño de la arquitectura del proyecto. La utilización de archivos de configuración centralizados, la separación entre entrenamiento e inferencia y la organización modular del código permiten que los distintos procesos se ejecuten de manera consistente, reduciendo la posibilidad de introducir diferencias involuntarias entre distintas ejecuciones del sistema.

Adicionalmente, el proyecto incorpora mecanismos para preservar el entorno de ejecución mediante el registro de las dependencias utilizadas durante el desarrollo. Esto facilita la reconstrucción del ambiente de trabajo y contribuye a garantizar que futuras ejecuciones produzcan resultados consistentes con los obtenidos durante la etapa de entrenamiento.

En conjunto, estas decisiones permiten que el modelo no sea únicamente un archivo entrenado, sino un artefacto completamente versionado y reproducible, preparado para integrarse de forma confiable dentro de un sistema orientado a producción.

### 10.2 Consistencia entre entrenamiento e inferencia

Desde las primeras etapas del diseño del sistema se adoptó como principio fundamental que el modelo debía utilizar, tanto durante el entrenamiento como durante la inferencia, únicamente la información que realmente estaría disponible antes del inicio de cada partido. Esta decisión condicionó la arquitectura completa del proyecto y dio origen a varias de las soluciones implementadas a lo largo de su desarrollo.

Durante la construcción del dataset histórico se prestó especial atención a evitar la incorporación de información futura dentro de las variables utilizadas para el entrenamiento. Si bien el proyecto trabaja sobre partidos ya disputados, cada observación fue construida utilizando exclusivamente información disponible hasta la fecha correspondiente a ese encuentro. Este criterio condicionó buena parte de la ingeniería de variables. Por ejemplo, las puntuaciones **ELO** se calcularon de forma secuencial, actualizando el rating de cada equipo únicamente con resultados previamente conocidos, mientras que las variables asociadas al valor de mercado de los jugadores utilizaron las cotizaciones históricas correspondientes al momento en que se disputó cada partido y no los valores actuales disponibles en las bases de datos. Este enfoque evita la incorporación de información futura durante el entrenamiento, fenómeno conocido como *Data Leakage*.

El mismo principio fue mantenido durante la etapa de inferencia. En lugar de desarrollar un proceso independiente para generar las predicciones, el sistema reutiliza la misma representación del problema empleada durante el entrenamiento, utilizando idénticas definiciones de variables y los mismos criterios de transformación de los datos. Asimismo, el conjunto de características utilizado por el modelo se exporta junto con el artefacto entrenado y es validado antes de cada predicción, garantizando que el modelo reciba exactamente la información para la cual fue construido.

En la literatura especializada, las discrepancias entre la información utilizada durante el entrenamiento y aquella disponible durante la inferencia se conocen como *Training-Serving Skew*. Si bien el proyecto no implementa un sistema automático de monitoreo para detectar este fenómeno, la arquitectura fue diseñada desde su concepción para minimizar su aparición mediante la reutilización de la misma representación del problema a lo largo de todo el ciclo de vida del modelo.

De esta forma, la consistencia entre entrenamiento e inferencia deja de ser una verificación posterior para convertirse en un principio arquitectónico que guía tanto la construcción del dataset como el funcionamiento del sistema en producción.

### 10.3 Calidad de los datos

La calidad de los datos constituye uno de los factores más importantes para garantizar el correcto funcionamiento de un sistema de Machine Learning. En este proyecto, dicho aspecto no se limitó a la detección de valores faltantes o registros inconsistentes, sino que fue considerado durante todo el proceso de construcción del dataset.

A lo largo del pipeline histórico se incorporaron distintas etapas de validación destinadas a asegurar la consistencia de la información utilizada para el entrenamiento. Estas validaciones abarcaron tanto la verificación de los datos obtenidos mediante los procesos de scraping como la correcta integración de las diferentes fuentes empleadas para construir las variables del modelo. Cuando determinada información no cumplía con los criterios establecidos o no era posible reconstruirla de manera confiable, los registros correspondientes eran descartados o tratados de forma consistente antes de incorporarse al dataset final.

Un aspecto particularmente relevante fue la construcción de las variables derivadas de los jugadores. Dado que la información provenía de distintas fuentes y debía vincularse mediante un proceso de correspondencia entre jugadores, se realizaron controles específicos sobre la cobertura alcanzada por el *player mapping* y sobre la cantidad de futbolistas efectivamente identificados en cada equipo. Estas verificaciones permitieron cuantificar la calidad de la información disponible y evaluar el impacto potencial de los datos faltantes sobre las variables generadas.

Asimismo, tanto durante el entrenamiento como durante la inferencia, el sistema verifica la disponibilidad de las variables requeridas por el modelo antes de generar una predicción. Este mecanismo reduce el riesgo de ejecutar el modelo sobre datos incompletos o inconsistentes y contribuye a preservar la confiabilidad del proceso de inferencia.

En conjunto, estas decisiones permitieron construir un pipeline robusto frente a la calidad variable de las fuentes de información utilizadas, favoreciendo la generación de un dataset consistente y adecuado para el entrenamiento y la operación del sistema.

### 10.4 Escalabilidad y mantenibilidad

Durante el diseño del proyecto se buscó que la incorporación de nuevas funcionalidades pudiera realizarse con un impacto mínimo sobre los componentes ya existentes. Para ello se adoptó una arquitectura modular, basada en la separación de responsabilidades y en la definición de interfaces claras entre los distintos procesos que conforman el sistema.

Esta organización facilita la evolución del proyecto en diferentes dimensiones. La incorporación de nuevas competiciones, nuevas fuentes de información, nuevas familias de variables o incluso nuevos algoritmos de entrenamiento puede realizarse de manera localizada, reutilizando gran parte de la infraestructura desarrollada sin necesidad de modificar el funcionamiento general del sistema.

La separación entre entrenamiento, inferencia y adquisición de datos también contribuye a la mantenibilidad del proyecto. Cada uno de estos procesos puede evolucionar de manera relativamente independiente, permitiendo introducir mejoras o correcciones sin afectar el resto de la arquitectura. Como consecuencia, el sistema resulta más sencillo de mantener, probar y extender a medida que aumentan sus funcionalidades.

Si bien la versión actual representa una primera aproximación a un sistema de Machine Learning en producción, la arquitectura propuesta fue concebida para facilitar futuras ampliaciones, proporcionando una base sólida sobre la cual continuar desarrollando nuevas capacidades sin necesidad de rediseñar los componentes principales del proyecto.

### 10.5 Limitaciones actuales

Si bien la arquitectura desarrollada incorpora numerosos principios propios de un sistema de Machine Learning orientado a producción, la versión actual del proyecto representa una primera aproximación al problema planteado y, como tal, presenta algunas limitaciones que constituyen oportunidades de mejora para futuras versiones.

Desde el punto de vista del modelo predictivo, la representación utilizada se basa en la información disponible antes de cada partido, pero no incorpora factores dinámicos que pueden influir significativamente en el resultado final, como lesiones de último momento, sanciones, condiciones climáticas o cambios tácticos definidos inmediatamente antes del encuentro. La incorporación de este tipo de información constituye una posible línea de evolución del sistema.

Asimismo, si bien el proyecto contempla la actualización de los datos históricos y el reentrenamiento del modelo, estos procesos se ejecutan actualmente de forma manual. Una versión futura podría incorporar mecanismos automáticos de monitoreo, detección de degradación del desempeño y reentrenamiento periódico del modelo, aproximando aún más el sistema a un entorno de operación continuo.

Finalmente, la arquitectura fue diseñada para facilitar la incorporación de nuevas fuentes de información y nuevas competiciones. Esto abre la posibilidad de ampliar progresivamente la cobertura del sistema y enriquecer la representación del problema sin modificar los principios fundamentales sobre los cuales fue construido el proyecto.

Lejos de representar deficiencias del sistema, estas limitaciones reflejan el alcance definido para la presente versión y constituyen la base sobre la cual podrán desarrollarse futuras mejoras tanto desde el punto de vista del modelo como de la infraestructura de producción.

## 11. API REST

La construcción del modelo no completa por sí sola la puesta en producción del sistema, sino que para que el modelo pueda ser utilizado por otros procesos, usuarios o aplicaciones, es necesario exponerlo mediante una interfaz clara y estable. Con este propósito se desarrolló una API REST que permite consumir el modelo campeón sin depender directamente de los scripts internos del proyecto.

La API fue implementada utilizando FastAPI, lo que permitió definir endpoints específicos para consultar información del modelo, explorar los partidos disponibles y generar predicciones tanto individuales como por lotes. Esta decisión permitió separar la lógica interna de inferencia de la forma en que otros sistemas interactúan con el modelo.

Una de las decisiones más importantes fue ofrecer dos formas de consumo. Por un lado, se expusieron endpoints técnicos que permiten predecir a partir de identificadores de partidos o enviando directamente las variables requeridas por el modelo. Por otro lado, se incorporaron endpoints más orientados al uso del dominio, permitiendo consultar competiciones, equipos disponibles y generar predicciones a partir del nombre de los equipos participantes.

Esta mejora de usabilidad permitió que la API dejara de depender exclusivamente de identificadores internos y pudiera utilizarse de una forma más natural para un usuario final. En lugar de requerir que el usuario conozca el match_id de un partido, el sistema permite seleccionar una competición, consultar los equipos disponibles y solicitar una predicción indicando equipo local y visitante.

La API también incorpora validación de entradas mediante esquemas definidos con Pydantic, lo que permite controlar la estructura de los datos recibidos antes de ejecutar el modelo. Además, FastAPI genera automáticamente documentación interactiva mediante Swagger/OpenAPI, facilitando la prueba de los endpoints y reduciendo la necesidad de documentación manual adicional.

En conjunto, la API REST convierte al modelo entrenado en un servicio reutilizable, documentado y preparado para integrarse con aplicaciones externas o procesos automatizados de predicción.

## 12. Docker

Una vez desarrollada la API, el siguiente desafío consistió en garantizar que el sistema pudiera ejecutarse de manera consistente en distintos entornos. En proyectos de Machine Learning, las diferencias entre versiones de Python, dependencias, librerías del sistema operativo o rutas de archivos pueden generar errores difíciles de reproducir. Por este motivo se decidió containerizar la aplicación utilizando Docker.

La utilización de Docker permitió encapsular en una única imagen todos los elementos necesarios para ejecutar el servicio de inferencia: código fuente, dependencias, modelo campeón y dataset de scoring. De esta forma, la API puede ejecutarse dentro de un entorno controlado, reduciendo la dependencia de la configuración específica de la máquina donde se despliegue.

La containerización también contribuye a la reproducibilidad del sistema. Una vez construida la imagen, el servicio puede levantarse mediante un comando estándar y exponer la API en el puerto configurado, permitiendo acceder a la documentación interactiva y a los endpoints de predicción de la misma manera que en el entorno local de desarrollo.

Desde el punto de vista del despliegue, Docker constituye una base natural para futuras etapas del proyecto. La misma imagen puede utilizarse posteriormente en plataformas cloud, servicios de contenedores o entornos de integración continua, simplificando la transición desde el desarrollo local hacia un ambiente productivo.

En la versión actual, Docker fue utilizado para validar la ejecución local de la API dentro de un contenedor. Si bien aún no se implementó un despliegue cloud completo, la aplicación quedó preparada para avanzar hacia esa etapa sin modificar la lógica principal del sistema.

## 13. Discusión

Más que la implementación de un modelo de clasificación, el principal resultado de este proyecto fue el proceso de diseño que permitió transformar un problema complejo en un sistema de Machine Learning reproducible y preparado para producción. A lo largo del desarrollo fue necesario tomar decisiones relacionadas con la adquisición de datos, la representación del problema, la ingeniería de variables, la selección de modelos y el diseño de la arquitectura del sistema. En conjunto, estas decisiones tuvieron un impacto mucho mayor sobre el resultado final que la simple elección de un algoritmo de clasificación.

Este capítulo reflexiona sobre las principales decisiones adoptadas durante el proyecto, analizando sus fortalezas, las limitaciones de la solución desarrollada y las oportunidades de evolución que deja abiertas la arquitectura propuesta. Más que presentar nuevos resultados, el objetivo es discutir las implicancias de las decisiones tomadas y sintetizar los principales aprendizajes obtenidos durante el desarrollo del sistema.

### 13.1 Aprendizajes del proceso de diseño

Una de las principales enseñanzas obtenidas durante el desarrollo del proyecto fue comprender que la calidad de un sistema de Machine Learning depende tanto del proceso de diseño como del algoritmo finalmente seleccionado. Si bien el entrenamiento permitió identificar un modelo con buen desempeño, el recorrido realizado mostró que las decisiones adoptadas en etapas mucho más tempranas tuvieron un impacto decisivo sobre el resultado alcanzado.

El primer aprendizaje estuvo relacionado con la construcción del dataset. Desarrollar una base de datos propia implicó un esfuerzo considerable de adquisición, integración y validación de información proveniente de distintas fuentes. Sin embargo, este trabajo permitió controlar completamente la representación del problema, incorporar conocimiento específico del dominio y construir variables imposibles de obtener a partir de datasets ya procesados. En retrospectiva, esta decisión constituyó uno de los pilares fundamentales del proyecto.

Un segundo aprendizaje fue reconocer la importancia de la representación del problema. Inicialmente podría pensarse que el rendimiento del sistema dependería principalmente del algoritmo de clasificación utilizado. No obstante, los distintos experimentos realizados mostraron que la forma en que se describía cada partido tuvo una influencia igual o incluso mayor sobre el desempeño del modelo. La incorporación de variables relacionadas con la fortaleza de los equipos, las características agregadas de los jugadores y las comparaciones entre ambos planteles permitió construir una representación más rica y consistente del contexto previo a cada encuentro.

Desde el punto de vista de la ingeniería de software, otra enseñanza importante fue comprobar el valor de diseñar la arquitectura pensando desde el inicio en su utilización futura. La separación entre entrenamiento e inferencia, la modularización del código, el versionado de los modelos y la reutilización de los procesos de transformación incrementaron inicialmente el esfuerzo de desarrollo, pero facilitaron significativamente el mantenimiento del sistema, su reproducibilidad y su posterior despliegue mediante una API REST.

Finalmente, el proyecto permitió confirmar la importancia de definir un alcance realista para una primera versión del sistema. La idea inicial contemplaba la construcción de una herramienta capaz de analizar el impacto de modificaciones en la composición de los planteles sobre el resultado esperado de un partido. Durante el desarrollo fue necesario acotar este objetivo para concentrarse en la construcción de un sistema robusto de predicción de encuentros individuales. Lejos de representar una renuncia al objetivo original, esta decisión permitió desarrollar una base sólida sobre la cual será posible incorporar nuevas capacidades en versiones futuras.

En conjunto, estos aprendizajes refuerzan una idea que atravesó todo el proyecto: el desarrollo de un sistema de Machine Learning no consiste únicamente en entrenar un modelo con buenas métricas, sino en diseñar cuidadosamente la representación del problema, la calidad de los datos y la arquitectura que permitirá que ese modelo pueda utilizarse y evolucionar de manera confiable a lo largo del tiempo.

### 13.2 Fortalezas de la solución

Una de las principales fortalezas de la solución desarrollada es que logra integrar en un mismo sistema aspectos propios de la Ciencia de Datos y de la Ingeniería de Software. A lo largo del proyecto no solo se buscó obtener un modelo con buen desempeño predictivo, sino también construir una arquitectura que permitiera mantenerlo, reproducirlo y utilizarlo en un contexto similar al de un entorno de producción.

Desde el punto de vista metodológico, la construcción de un dataset propio y el desarrollo de una representación del partido basada en la información de los jugadores permitieron incorporar conocimiento específico del dominio al proceso de aprendizaje. Esta estrategia ofreció una mayor flexibilidad para diseñar variables relevantes y evitó depender exclusivamente de datasets previamente elaborados para otros propósitos.

Otra fortaleza importante radica en la organización del sistema. La separación entre adquisición de datos, entrenamiento e inferencia permitió desacoplar procesos con objetivos diferentes y facilitó tanto el mantenimiento del proyecto como la incorporación de nuevas funcionalidades. Esta arquitectura también favoreció la reutilización de componentes y simplificó el desarrollo de la API REST y del pipeline de inferencia.

Asimismo, el proyecto incorporó desde sus primeras etapas prácticas orientadas a la reproducibilidad, como el versionado del modelo campeón, la conservación de los metadatos asociados al entrenamiento y la utilización de un entorno de ejecución reproducible mediante Docker. Si bien estas decisiones no impactan directamente sobre las métricas del modelo, incrementan significativamente la confiabilidad y mantenibilidad del sistema.

Finalmente, una de las fortalezas más importantes de la solución propuesta es que la arquitectura desarrollada no se encuentra limitada al problema específico resuelto en esta primera versión. La forma en que fueron representados los equipos, las variables y los procesos deja preparada una base sólida para incorporar nuevas fuentes de información, ampliar la cobertura del sistema y desarrollar funcionalidades adicionales sin necesidad de rediseñar la estructura general del proyecto.

### 13.3 Limitaciones

Como toda primera versión de un sistema, la solución desarrollada presenta limitaciones que responden tanto a las características del problema como a las decisiones de alcance adoptadas durante el proyecto. En retrospectiva, muchas de estas limitaciones no representan deficiencias de la arquitectura, sino el resultado de priorizar la construcción de una base sólida sobre la cual continuar evolucionando el sistema.

Desde el punto de vista del modelo predictivo, la representación utilizada describe el estado de ambos equipos a partir de la información disponible antes de cada encuentro. En consecuencia, no incorpora factores altamente dinámicos que también pueden influir sobre el resultado de un partido, como lesiones de último momento, sanciones, cambios tácticos, condiciones climáticas o decisiones técnicas adoptadas inmediatamente antes del inicio del juego. La incorporación de este tipo de información podría enriquecer la representación del problema, aunque también incrementaría considerablemente la complejidad del proceso de adquisición y actualización de los datos.

Otra limitación está relacionada con el alcance funcional de esta primera versión. Si bien la representación construida se basa en las características de los jugadores que integran cada plantel, el sistema fue diseñado para responder una única pregunta: predecir el resultado esperado de un partido. Otras aplicaciones potenciales de esta representación, como el análisis de escenarios alternativos o la evaluación del impacto de modificaciones en la composición de los equipos, quedaron deliberadamente fuera del alcance del proyecto con el objetivo de concentrar los esfuerzos en la construcción de una solución robusta y reproducible.

Finalmente, algunos procesos propios de un entorno de producción aún requieren intervención manual, como la actualización de las fuentes de información o el reentrenamiento periódico del modelo. Si bien la arquitectura fue diseñada para facilitar estas tareas, una implementación completamente automatizada excedía los objetivos planteados para la presente versión.

En conjunto, estas limitaciones reflejan el alcance definido para el proyecto más que restricciones inherentes a la arquitectura desarrollada. Por este motivo, constituyen oportunidades concretas de evolución para futuras versiones del sistema antes que obstáculos para su utilización actual.

### 13.4 Trabajo futuro

La arquitectura desarrollada durante este proyecto fue concebida con el objetivo de facilitar su evolución hacia nuevas funcionalidades sin necesidad de modificar los principios fundamentales sobre los cuales fue construida. En este sentido, las posibilidades de trabajo futuro no consisten únicamente en mejorar el desempeño predictivo del modelo, sino principalmente en ampliar las capacidades del sistema a partir de la representación del problema ya desarrollada.

Una de las principales ventajas de la solución propuesta es que cada partido se representa a partir de atributos agregados de los jugadores y del contexto competitivo de ambos equipos, en lugar de depender exclusivamente de información histórica de los clubes. Esta decisión deja abierta la posibilidad de desarrollar herramientas de simulación capaces de estimar el impacto que tendrían modificaciones en la composición de los planteles antes de la disputa de un encuentro.

De esta forma, el modelo podría evolucionar desde una herramienta orientada exclusivamente a la predicción hacia un sistema de apoyo a la toma de decisiones deportivas; la posibilidad de incorporar o retirar jugadores de manera hipotética, recalcular las variables del equipo y evaluar cómo cambian las probabilidades estimadas permitiría analizar distintos escenarios de planificación deportiva, mercado de pases o conformación de planteles utilizando la misma arquitectura desarrollada en esta primera versión.

Asimismo, futuras versiones podrían incorporar nuevas fuentes de información relacionadas con lesiones, sanciones, condiciones climáticas, alineaciones confirmadas o variables tácticas, enriqueciendo progresivamente la representación del problema sin modificar la estructura general del sistema. Del mismo modo, la automatización de procesos como la actualización de los datos históricos, el monitoreo del desempeño del modelo y el reentrenamiento periódico permitiría aproximar aún más la solución a un entorno de operación continua.

En conjunto, estas líneas de evolución muestran que el principal resultado del proyecto no es únicamente el modelo obtenido, sino la construcción de una arquitectura flexible capaz de crecer junto con nuevas preguntas y nuevos escenarios de aplicación. En este sentido, la versión desarrollada constituye una base sólida sobre la cual continuar expandiendo las capacidades del sistema en futuras etapas de desarrollo.

# 14. Conclusiones

El objetivo inicial de este proyecto fue desarrollar un sistema capaz de predecir el resultado de partidos de fútbol utilizando información disponible antes de la disputa de cada encuentro. Sin embargo, a lo largo del desarrollo quedó en evidencia que este desafío trascendía ampliamente la construcción de un modelo de clasificación y requería resolver problemas relacionados con la adquisición de datos, la representación del dominio, la ingeniería de variables, la arquitectura del sistema y su preparación para un entorno de producción.

La solución desarrollada demuestra que es posible integrar información proveniente de múltiples fuentes para construir una representación consistente del estado de ambos equipos antes de un partido, entrenar un modelo reproducible y exponer sus capacidades mediante una arquitectura modular preparada para evolucionar. En este sentido, el principal aporte del proyecto no radica únicamente en las métricas alcanzadas por el modelo campeón, sino en la construcción de un sistema completo que integra procesos de adquisición de datos, entrenamiento, inferencia y despliegue siguiendo principios propios de Machine Learning en Producción.

Uno de los principales aprendizajes obtenidos fue comprender que muchas de las decisiones con mayor impacto sobre el resultado final fueron tomadas antes del entrenamiento del modelo. La calidad del dataset, la representación del problema y el diseño de la arquitectura demostraron ser tan importantes como la elección del algoritmo utilizado para realizar las predicciones.

Finalmente, la arquitectura propuesta deja abierta una línea de evolución natural para futuras versiones del sistema. La representación del partido basada en las características agregadas de los jugadores constituye una base sólida para desarrollar herramientas de simulación y apoyo a la toma de decisiones deportivas, ampliando progresivamente el alcance del proyecto más allá de la predicción de resultados.

En conjunto, el trabajo realizado permitió alcanzar los objetivos planteados para esta primera versión y establecer una plataforma flexible sobre la cual continuar desarrollando nuevas capacidades, manteniendo como eje central la construcción de soluciones de Machine Learning reproducibles, mantenibles y orientadas a producción.
