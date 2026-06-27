from pathlib import Path
from datetime import datetime
import json
import pandas as pd
from joblib import dump
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from src.config.project_config import (
    ROOT,
    MODEL_VERSION,
    RANDOM_STATE,
    REPORTS_DIR
)
from src.config.dataset_config import load_feature_set
from src.models.load_dataset import load_dataset


# =========================================================
# PATHS
# =========================================================

CHAMPION_DIR = ROOT / "models" / "champions" / MODEL_VERSION
CHAMPION_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = CHAMPION_DIR / "model.joblib"
METADATA_FILE = CHAMPION_DIR / "metadata.json"
README_FILE = CHAMPION_DIR / "README.md"


print("\nCHAMPION_DIR:", CHAMPION_DIR)


# =========================================================
# FEATURES (FROM CONFIG)
# =========================================================

FEATURE_SET_NAME = "top30"

top_features = load_feature_set(FEATURE_SET_NAME)


# =========================================================
# DATASET
# =========================================================

X, y, features, dataset_modified = load_dataset(
    selected_features=top_features
)

print(f"\nFeatures utilizadas: {len(features)}")


# =========================================================
# MODEL
# =========================================================

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

lr = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ))
])

model = StackingClassifier(
    estimators=[
        ("rf", rf),
        ("lr", lr)
    ],
    final_estimator=LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    ),
    stack_method="predict_proba",
    cv=5,
    n_jobs=-1
)


# =========================================================
# TRAIN
# =========================================================

print("\nEntrenando modelo campeón...")

model.fit(X, y)


# =========================================================
# SAVE MODEL
# =========================================================

dump(model, MODEL_FILE)

print("\nModelo guardado en:")
print(MODEL_FILE)


# =========================================================
# METADATA (CONSISTENTE CON CONFIG)
# =========================================================

metadata = {
    "version": MODEL_VERSION,
    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    "model": "Stacking Ensemble",

    "dataset": {
        "rows": int(len(X)),
        "timestamp": dataset_modified
    },

    "features": {
        "set": FEATURE_SET_NAME,
        "count": len(features)
    },

    "training": {
        "random_state": RANDOM_STATE
    },

    "target": "result",
    "n_classes": 3,

    "model_file": str(MODEL_FILE.name)
}


with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print("\nMetadata guardada.")


# =========================================================
# README
# =========================================================

readme_text = f"""
# {MODEL_VERSION}

Modelo campeón del proyecto.

## Arquitectura

Stacking Ensemble:
- Random Forest
- Logistic Regression
- Meta-model: Logistic Regression

## Features

Feature set: {FEATURE_SET_NAME}
Cantidad: {len(features)}

## Dataset

Observaciones: {len(X)}
Timestamp: {dataset_modified}

## Resultados

(TBD: provenientes de evaluación externa)

## Fecha

{datetime.now().strftime("%Y-%m-%d")}
"""


with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(readme_text.strip())


print("\nREADME generado.")

print("\n" + "=" * 60)
print("MODELO CAMPEÓN EXPORTADO")
print("=" * 60)
print("\nUbicación:", CHAMPION_DIR)