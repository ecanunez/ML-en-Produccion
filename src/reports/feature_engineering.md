# Feature Engineering

## Proyecto

Predicción de resultados de partidos de fútbol utilizando información de mercado, forma reciente, perfiles de jugadores y ratings Elo.

---

# Dataset Base

El dataset original contiene variables relacionadas con:

## Valor de mercado

* home_team_market_value
* away_team_market_value

### Por posición

* home_GK_market_value_sum

* home_DEF_market_value_sum

* home_MID_market_value_sum

* home_ATT_market_value_sum

* away_GK_market_value_sum

* away_DEF_market_value_sum

* away_MID_market_value_sum

* away_ATT_market_value_sum

---

## Forma reciente (últimos 5 partidos)

### Equipo local

* home_points_last5
* home_win_rate_last5
* home_gf_last5
* home_ga_last5
* home_gd_last5

### Equipo visitante

* away_points_last5
* away_win_rate_last5
* away_gf_last5
* away_ga_last5
* away_gd_last5

---

## Elo Rating

* home_elo
* away_elo

---

## Variables derivadas originales

### Diferencias de valor de mercado

* market_value_diff
* GK_value_diff
* DEF_value_diff
* MID_value_diff
* ATT_value_diff

### Diferencias de forma reciente

* points_diff
* win_rate_diff
* gd_diff

### Diferencia Elo

* elo_diff

---

# Feature Engineering v1

## Fecha

2026-06-19

---

## Objetivo

Incorporar señales adicionales relacionadas con rendimiento reciente, calidad relativa de los equipos y completitud de la información obtenida durante el scraping.

---

## gf_diff

Diferencia de goles a favor en los últimos 5 partidos.

```python
gf_diff = (
    home_gf_last5
    - away_gf_last5
)
```

Interpretación:

* Valores positivos favorecen al equipo local.
* Valores negativos favorecen al equipo visitante.

---

## ga_diff

Diferencia de goles en contra en los últimos 5 partidos.

```python
ga_diff = (
    home_ga_last5
    - away_ga_last5
)
```

Interpretación:

* Valores negativos indican una defensa local más sólida.
* Valores positivos indican una defensa visitante más sólida.

---

## players_found_diff

Diferencia entre la cantidad de jugadores encontrados para cada equipo durante el scraping.

```python
players_found_diff = (
    home_players_found
    - away_players_found
)
```

Objetivo:

* Capturar diferencias en la calidad o completitud de la información disponible para cada plantilla.

---

## market_value_ratio

Relación entre el valor de mercado del equipo local y el visitante.

```python
market_value_ratio = (
    home_team_market_value
    /
    (away_team_market_value + 1)
)
```

Objetivo:

* Capturar relaciones relativas entre equipos que no pueden representarse únicamente mediante diferencias absolutas.

Ejemplo:

| Local  | Visitante | Diferencia | Ratio |
| ------ | --------: | ---------: | ----: |
| 200 M€ |    100 M€ |     100 M€ |   2.0 |
| 600 M€ |    500 M€ |     100 M€ |   1.2 |

Aunque la diferencia absoluta es la misma, la relación competitiva es distinta.

---

## Resultados

### Dataset base

* Features: 39
* Accuracy: 0.5119
* F1 Macro: 0.4751

### Dataset con Feature Engineering v1

* Features: 43
* Accuracy: 0.5127
* F1 Macro: 0.4761

---

## Conclusiones

1. La variable más importante continuó siendo `elo_diff`.

2. `market_value_ratio` aportó información complementaria a `market_value_diff`.

3. `players_found_diff` y `ga_diff` mostraron señal predictiva útil.

4. La mejora global fue moderada (+0.0010 F1 Macro), indicando que el modelo ya capturaba gran parte de la información disponible.

---

# Feature Engineering v2 — Perfiles Internacionales y Balance de Equipos

## Fecha

2026-06-20

---

## Objetivo

Mejorar la identificación de partidos equilibrados y aumentar la capacidad predictiva mediante información individual de los jugadores convocados.

---

## Perfiles internacionales

Archivo:

player_profile_features.parquet

### Edad

* home_avg_age
* away_avg_age
* age_diff

Hipótesis:

Equipos más maduros podrían rendir mejor en contextos internacionales.

---

### Experiencia internacional

* home_avg_caps
* away_avg_caps
* caps_diff

Hipótesis:

La experiencia acumulada representa conocimiento competitivo en escenarios de alta exigencia.

---

### Producción goleadora internacional

* home_avg_int_goals
* away_avg_int_goals
* int_goals_diff

Hipótesis:

Jugadores con historial goleador internacional aportan capacidad diferencial para definir encuentros.

---

### Altura promedio

* home_avg_height
* away_avg_height
* height_diff

Hipótesis:

La estatura promedio puede representar ventajas físicas y tácticas.

---

### Valor promedio por jugador

* home_avg_player_value
* away_avg_player_value

Hipótesis:

La calidad media del plantel contiene información complementaria al valor total del equipo.

---

## Variables de equilibrio competitivo

Archivo:

player_balance_features.parquet

### Diferencias absolutas

* abs_caps_diff
* abs_age_diff
* abs_int_goals_diff
* abs_market_value_diff
* abs_GK_value_diff
* abs_DEF_value_diff
* abs_MID_value_diff
* abs_ATT_value_diff
* abs_elo_diff
* abs_points_diff
* abs_gd_diff

Hipótesis:

Los empates ocurren con mayor frecuencia cuando la diferencia real entre equipos es pequeña.

---

### Indicadores binarios de equilibrio

* elo_balanced
* market_balanced
* caps_balanced
* age_balanced

Hipótesis:

Partidos con diferencias inferiores a determinados umbrales presentan mayor probabilidad de empate.

---

### Variables agregadas

* balance_score
* high_balance_match

Hipótesis:

La combinación de múltiples indicadores de equilibrio puede capturar partidos cerrados.

---

## Resultados observados

### Antes de incorporar balance features

* Accuracy: 0.5107
* F1 Macro: 0.4792

### Después de incorporar balance features

* Accuracy: 0.5147
* F1 Macro: 0.4830

---

## Mejora observada

* +0.0040 Accuracy
* +0.0038 F1 Macro

---

## Variables destacadas

* elo_diff
* market_value_diff
* caps_diff
* abs_elo_diff
* home_avg_player_value
* away_avg_player_value

Las nuevas variables relacionadas con experiencia internacional y equilibrio competitivo aparecieron entre las más importantes del modelo.

---

## Conclusión

Las diferencias absolutas entre equipos aportan información útil y refuerzan la hipótesis de que el equilibrio competitivo es un factor relevante para explicar empates.

---

# Feature Selection

## Fecha

2026-06-21

---

## Objetivo

Evaluar si todas las variables generadas aportan información útil o si existe un subconjunto más pequeño capaz de mantener o mejorar el desempeño.

---

## Metodología

Las variables fueron ordenadas utilizando la importancia obtenida mediante Random Forest Tuned.

Posteriormente se entrenó el mismo modelo utilizando:

* Top 10 variables
* Top 20 variables
* Top 30 variables
* Top 40 variables
* Top 50 variables
* Todas las variables

Se mantuvieron constantes:

* train_test_split
* random_state
* hiperparámetros del modelo

---

## Resultados

| Experimento | Features |   F1 Macro |
| ----------- | -------: | ---------: |
| Top10       |       10 |     0.4724 |
| Top20       |       20 |     0.4750 |
| Top30       |       30 |     0.4760 |
| Top40       |       40 | **0.4870** |
| Top50       |       50 |     0.4798 |
| All         |       72 |     0.4830 |

---

## Hallazgo principal

El mejor desempeño no se obtuvo utilizando todas las variables disponibles.

El mejor resultado se alcanzó con únicamente las 40 variables más importantes.

* Top40 → F1 Macro = 0.4870
* All Features → F1 Macro = 0.4830

La reducción de dimensionalidad eliminó ruido y variables redundantes.

---

## Variables más importantes

Top 10:

1. elo_diff
2. market_value_diff
3. caps_diff
4. DEF_value_diff
5. home_avg_player_value
6. away_avg_player_value
7. abs_elo_diff
8. MID_value_diff
9. away_team_market_value
10. int_goals_diff

---

## Conclusión

La selección de variables permitió obtener el mejor resultado alcanzado hasta el momento.

### Mejor modelo actual

* Accuracy: 0.5147
* F1 Macro: 0.4870

La mayor parte de la señal predictiva está concentrada en aproximadamente 40 variables relacionadas con:

* Elo Rating
* Valor de mercado
* Diferencias por posición
* Experiencia internacional
* Producción goleadora
* Equilibrio competitivo

---

# Próximos pasos

## Fase 4 — Ingeniería avanzada de variables

### Predicción de empates

* Nuevos indicadores de equilibrio competitivo
* Diferencias relativas entre equipos
* Variables derivadas de probabilidades Elo

### Forma reciente avanzada

* Últimos 3 partidos
* Últimos 10 partidos
* Tendencias de rendimiento

### Valor de mercado

* Ratios por posición
* Concentración del valor dentro del plantel
* Dependencia de jugadores estrella

### Elo Rating

* Probabilidad implícita de victoria local
* Probabilidad implícita de victoria visitante
* Variables derivadas del diferencial Elo

### Interpretabilidad

* Permutation Importance
* SHAP Values
* Recursive Feature Elimination (RFE)

---

## Estado actual del proyecto

El principal cuello de botella ya no parece ser la cantidad de variables disponibles.

La evidencia obtenida mediante Feature Selection indica que las futuras mejoras probablemente provendrán de la construcción de variables más informativas y específicas del dominio futbolístico, en lugar de simplemente aumentar el número total de features.
