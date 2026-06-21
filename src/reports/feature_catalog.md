# Feature Catalog

## player_match_stats.parquet

Variables: 10

### Forma reciente

* home_points_last5

* away_points_last5

* home_win_rate_last5

* away_win_rate_last5

* home_gf_last5

* away_gf_last5

* home_ga_last5

* away_ga_last5

* home_gd_last5

* away_gd_last5

### Diferencias derivadas

* points_diff
* win_rate_diff
* gd_diff

Objetivo:

Representar el rendimiento reciente de los equipos utilizando los últimos 5 partidos disputados.

Estado:

✅ Utilizada en modelo final.

---

## team_strength_features.parquet

Variables: 24

### Valor total del plantel

* home_team_market_value
* away_team_market_value
* market_value_diff

### Porteros

* home_GK_market_value_sum
* away_GK_market_value_sum
* GK_value_diff

### Defensas

* home_DEF_market_value_sum
* away_DEF_market_value_sum
* DEF_value_diff

### Mediocampo

* home_MID_market_value_sum
* away_MID_market_value_sum
* MID_value_diff

### Ataque

* home_ATT_market_value_sum
* away_ATT_market_value_sum
* ATT_value_diff

### Promedios

* home_team_market_value_mean

* away_team_market_value_mean

* home_GK_market_value_mean

* away_GK_market_value_mean

* home_DEF_market_value_mean

* away_DEF_market_value_mean

* home_MID_market_value_mean

* away_MID_market_value_mean

* home_ATT_market_value_mean

* away_ATT_market_value_mean

Objetivo:

Medir calidad económica y deportiva de los planteles.

Estado:

✅ Utilizada en modelo final.

---

## elo_features.parquet

Variables: 3

* home_elo
* away_elo
* elo_diff

Objetivo:

Representar fuerza histórica internacional mediante ratings Elo.

Estado:

✅ Utilizada en modelo final.

---

## player_profile_features.parquet

Variables: 13

### Edad

* home_avg_age
* away_avg_age
* age_diff

### Altura

* home_avg_height
* away_avg_height
* height_diff

### Experiencia internacional

* home_avg_caps
* away_avg_caps
* caps_diff

### Producción goleadora internacional

* home_avg_int_goals
* away_avg_int_goals
* int_goals_diff

### Valor promedio por jugador

* home_avg_player_value
* away_avg_player_value

Objetivo:

Representar experiencia, características físicas y calidad promedio de los jugadores convocados.

Estado:

✅ Utilizada en modelo final.

---

## player_balance_features.parquet

Variables: 17

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

### Indicadores de equilibrio

* elo_balanced

* market_balanced

* caps_balanced

* age_balanced

### Variables agregadas

* balance_score

* high_balance_match

Objetivo:

Detectar partidos potencialmente equilibrados y aumentar la capacidad de identificar empates.

Estado:

✅ Utilizada en modelo final.

---

# Variables más importantes

Según Random Forest Tuned y Feature Selection (2026-06-21).

## Top 10

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

Estas variables concentran una parte importante de la señal predictiva del modelo.

---

# Resumen

| Archivo                 | Variables |
| ----------------------- | --------: |
| player_match_stats      |        13 |
| team_strength_features  |        24 |
| elo_features            |         3 |
| player_profile_features |        13 |
| player_balance_features |        17 |

| Métrica                      |  Valor |
| ---------------------------- | -----: |
| Features totales disponibles |     72 |
| Mejor subconjunto encontrado |     40 |
| Accuracy                     | 0.5147 |
| F1 Macro                     | 0.4870 |

---

# Estado del Proyecto

## Mejor modelo actual

Random Forest Tuned + Feature Selection

### Resultados

* Accuracy: 0.5147
* F1 Macro: 0.4870

### Hallazgo principal

La mayor parte de la señal predictiva se concentra en aproximadamente 40 variables relacionadas con:

* Elo Rating
* Valor de mercado
* Diferencias por posición
* Experiencia internacional
* Producción goleadora
* Equilibrio competitivo

Las futuras mejoras deberían enfocarse en la construcción de variables más informativas y no únicamente en aumentar la cantidad total de features.
