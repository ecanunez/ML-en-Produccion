# Feature Pipeline & Model Training Architecture

## Fecha
2026-06-27

---

## 1. Objetivo del sistema

Estandarizar el pipeline de machine learning para:

- eliminar duplicación de lógica
- eliminar hardcoding de features
- desacoplar feature engineering, selección y training
- asegurar reproducibilidad de experimentos
- permitir comparación consistente de modelos

---

## 2. Arquitectura general del pipeline

```
Feature Engineering
        ↓
Dataset de entrenamiento
        ↓
Feature Selection (Top-N)
        ↓
Feature Set Registry
        ↓
Model Training + Evaluation
```

---

## 3. Feature Engineering (Generación de variables)

📍 `src/features/engineering/`

### Responsabilidad
- Elo features
- market value features
- player profiles
- balance features
- interaction features

### Output
`training_dataset.parquet`

---

## 4. Feature Selection (Ranking + Top-N)

📍 `src/features/selection/build_feature_sets.py`

### Proceso
1. Entrenar Random Forest
2. Calcular feature importance
3. Ordenar variables
4. Generar Top-N

### Subconjuntos
- Top10
- Top20
- Top30
- Top40
- Top50

### Outputs
- feature_importance_ranking.csv
- top10_features.csv
- top20_features.csv
- top30_features.csv
- top40_features.csv
- top50_features.csv

---

## 5. Feature Set Registry

📍 `src/config/feature_sets.py`

### Feature sets disponibles
- top10
- top20
- top30
- top40
- top50
- all

### Uso
```python
features = load_feature_set("top30")
```

---

## 6. Model Registry

📍 `src/models/model_registry.py`

### Modelos
- Random Forest
- XGBoost
- LightGBM
- Logistic Regression
- Soft Voting
- Stacking

---

## 7. Training Pipeline

📍 `train.py`

### Ejecución
```bash
python train.py --model rf --features top40
```

### Flujo
load features → load dataset → split → train → evaluate

---

## 8. Flujo completo

```
Feature Engineering → Dataset → Feature Selection → Registry → Training → Evaluation
```

---

## 9. Decisiones de diseño

- Separación de responsabilidades
- Feature selection por importance
- Feature sets reproducibles
- Eliminación de hardcoding

---

## 10. Beneficios

### Antes
- scripts duplicados
- hardcoding
- baja reproducibilidad

### Después
- modular
- reproducible
- escalable

---

## 11. Conclusión

Pipeline estructurado de ML con separación clara entre:

features → selection → models → training
