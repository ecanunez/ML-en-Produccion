# Feature Catalog

## player_match_stats.parquet

Variables: 9

### Forma reciente

* home_points_last5

* away_points_last5

* points_diff

* home_gf_last5

* away_gf_last5

* home_ga_last5

* away_ga_last5

* home_gd_last5

* away_gd_last5

* gd_diff

Objetivo: representar rendimiento reciente de los equipos.

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

Objetivo: medir calidad económica y deportiva de los planteles.

---

## elo_features.parquet

Variables: 3

* home_elo
* away_elo
* elo_diff

Objetivo: representar fuerza histórica internacional.

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

### Goles internacionales

* home_avg_int_goals
* away_avg_int_goals
* int_goals_diff

### Valor promedio

* home_avg_player_value
* away_avg_player_value

Objetivo: representar experiencia y características medias de los jugadores.

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

Objetivo: detectar partidos potencialmente equilibrados y aumentar la capacidad de identificar empates.

---

# Resumen

| Archivo                 | Variables |
| ----------------------- | --------: |
| player_match_stats      |         9 |
| team_strength_features  |        24 |
| elo_features            |         3 |
| player_profile_features |        13 |
| player_balance_features |        17 |

Total aproximado de features generadas: 66+
