# Model History

## 2026-06-19 — Incorporación de perfiles internacionales

### Nuevas variables

* home_avg_age
* away_avg_age
* age_diff
* home_avg_caps
* away_avg_caps
* caps_diff
* home_avg_int_goals
* away_avg_int_goals
* int_goals_diff

### Resultados

#### Logistic Regression

Accuracy: 0.5361

F1 Macro: 0.3993

#### Random Forest

Accuracy: 0.5262

F1 Macro: 0.4876

#### Random Forest Tuned

Accuracy: 0.5183

F1 Macro: 0.4857

#### Hist Gradient Boosting

Accuracy: 0.5369

F1 Macro: 0.4048

### Conclusiones

Las variables relacionadas con experiencia internacional (caps) y edad promedio aparecen entre las variables más importantes del modelo.

La incorporación de perfiles internacionales aporta señal predictiva adicional y mejora el desempeño respecto a versiones anteriores.
