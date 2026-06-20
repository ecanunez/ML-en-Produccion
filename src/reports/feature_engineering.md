# Feature Engineering

## Proyecto

Predicción de resultados de partidos de fútbol utilizando información de mercado, forma reciente y ratings Elo.

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

Fecha: 19/06/2026

Se incorporaron nuevas variables con el objetivo de capturar información adicional sobre equilibrio competitivo, capacidad ofensiva y calidad de los datos obtenidos durante el scraping.

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

Diferencia entre la cantidad de jugadores encontrados para cada equipo durante el proceso de scraping.

```python
players_found_diff = (
    home_players_found
    - away_players_found
)
```

Objetivo:

* Capturar posibles diferencias en la calidad o completitud de la información disponible para cada plantilla.

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

Aunque la diferencia es la misma, la relación competitiva es distinta.

---

# Resultados

## Random Forest Tuned

### Dataset base

* Features: 39
* Accuracy: 0.5119
* F1 Macro: 0.4751

### Dataset con Feature Engineering v1

* Features: 43
* Accuracy: 0.5127
* F1 Macro: 0.4761

---

# Conclusiones

1. La variable más importante del modelo continúa siendo `elo_diff`.

2. `market_value_ratio` se incorporó inmediatamente entre las variables con mayor importancia, indicando que aporta información complementaria a `market_value_diff`.

3. `players_found_diff` y `ga_diff` también mostraron señal predictiva útil.

4. La mejora global fue moderada (+0.0010 en F1 Macro), lo que sugiere que el modelo ya captura gran parte de la información disponible en las variables originales.

5. Las próximas iteraciones de Feature Engineering deberían enfocarse en mejorar la predicción de empates, actualmente la clase más difícil para el modelo.

# Feature Engineering

## Proyecto

Predicción de resultados de partidos de fútbol utilizando información de mercado, forma reciente y ratings Elo.

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

Fecha: 19/06/2026

Se incorporaron nuevas variables con el objetivo de capturar información adicional sobre equilibrio competitivo, capacidad ofensiva y calidad de los datos obtenidos durante el scraping.

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

Diferencia entre la cantidad de jugadores encontrados para cada equipo durante el proceso de scraping.

```python
players_found_diff = (
    home_players_found
    - away_players_found
)
```

Objetivo:

* Capturar posibles diferencias en la calidad o completitud de la información disponible para cada plantilla.

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

Aunque la diferencia es la misma, la relación competitiva es distinta.

---

# Resultados

## Random Forest Tuned

### Dataset base

* Features: 39
* Accuracy: 0.5119
* F1 Macro: 0.4751

### Dataset con Feature Engineering v1

* Features: 43
* Accuracy: 0.5127
* F1 Macro: 0.4761

---

# Conclusiones

1. La variable más importante del modelo continúa siendo `elo_diff`.

2. `market_value_ratio` se incorporó inmediatamente entre las variables con mayor importancia, indicando que aporta información complementaria a `market_value_diff`.

3. `players_found_diff` y `ga_diff` también mostraron señal predictiva útil.

4. La mejora global fue moderada (+0.0010 en F1 Macro), lo que sugiere que el modelo ya captura gran parte de la información disponible en las variables originales.

5. Las próximas iteraciones de Feature Engineering deberían enfocarse en mejorar la predicción de empates, actualmente la clase más difícil para el modelo.

# Feature Engineering v2 — Perfiles Internacionales y Balance de Equipos

## Fecha

2026-06-20

---

## Objetivo

Mejorar la capacidad del modelo para identificar partidos equilibrados y aumentar la detección de empates utilizando información individual de los jugadores convocados.

---

## Nuevas variables de perfiles internacionales

Archivo:

player_profile_features.parquet

### Edad

* home_avg_age
* away_avg_age
* age_diff

Hipótesis:

Equipos con jugadores más maduros y experimentados podrían obtener mejores resultados en competiciones internacionales.

### Experiencia internacional

* home_avg_caps
* away_avg_caps
* caps_diff

Hipótesis:

La cantidad de partidos internacionales disputados representa experiencia competitiva y conocimiento de escenarios de alta exigencia.

### Goles internacionales

* home_avg_int_goals
* away_avg_int_goals
* int_goals_diff

Hipótesis:

Los jugadores con mayor producción ofensiva internacional aportan capacidad diferencial para definir encuentros.

### Altura promedio

* home_avg_height
* away_avg_height
* height_diff

Hipótesis:

La estatura promedio puede reflejar ventajas físicas en determinados contextos tácticos.

### Valor promedio por jugador

* home_avg_player_value
* away_avg_player_value

Hipótesis:

La calidad media del plantel puede contener información complementaria al valor total del equipo.

---

## Variables de equilibrio entre equipos

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

### Indicadores binarios de equilibrio

* elo_balanced
* market_balanced
* caps_balanced
* age_balanced

Hipótesis:

Partidos con diferencias inferiores a determinados umbrales pueden presentar mayor probabilidad de empate.

### Variables agregadas

* balance_score
* high_balance_match

Hipótesis:

La combinación de múltiples indicadores de equilibrio podría capturar situaciones típicas de partidos cerrados.

---

## Resultados observados

Random Forest Tuned

Antes de balance features:

* Accuracy: 0.5107
* F1 Macro: 0.4792

Después de balance features:

* Accuracy: 0.5147
* F1 Macro: 0.4830

Mejora observada:

* +0.0040 Accuracy
* +0.0038 F1 Macro

Variables destacadas en Feature Importance:

* abs_elo_diff
* abs_market_value_diff
* abs_caps_diff

Conclusión:

Las diferencias absolutas entre equipos aportan información útil al modelo y refuerzan la hipótesis de que el equilibrio competitivo es un factor relevante para explicar los empates.
