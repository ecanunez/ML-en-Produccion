from pathlib import Path
from shutil import copyfile
from datetime import datetime
import json

import pandas as pd

from joblib import dump

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    StackingClassifier
)

from load_dataset import load_dataset

# =========================================================

# PATHS

# =========================================================

ROOT = Path(__file__).resolve().parents[2]

CHAMPION_DIR = (
    ROOT
    / "models"
    / "champions"
    / "v1.0_model_champion"
)

CHAMPION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TOP30_FILE = (
    ROOT
    / "src"
    / "reports"
    / "top30_features.csv"
)

MODEL_FILE = (
    CHAMPION_DIR
    / "model.joblib"
)

METADATA_FILE = (
    CHAMPION_DIR
    / "metadata.json"
)

README_FILE = (
    CHAMPION_DIR
    / "README.md"
)

print("\nROOT:")
print(ROOT)

print("\nCHAMPION_DIR:")
print(CHAMPION_DIR)

# =========================================================

# FEATURES

# =========================================================

top30_features = (
    pd.read_csv(TOP30_FILE)["feature"]
    .tolist()
)

# =========================================================

# DATASET

# =========================================================

X, y, features, dataset_modified = load_dataset(
    selected_features=top30_features
)

print(
    f"\nFeatures utilizadas: "
    f"{len(features)}"
)

# =========================================================

# BASE MODELS

# =========================================================

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

lr = Pipeline([
    (
        "scaler",
        StandardScaler()
        ),
    (
        "model",
        LogisticRegression(
            max_iter=5000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# =========================================================

# STACKING CHAMPION

# =========================================================

model = StackingClassifier(
    estimators=[
        ("rf", rf),
        ("lr", lr)
    ],
    final_estimator=LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=42
    ),
    stack_method="predict_proba",
    cv=5,
    n_jobs=-1
)

print("\nEntrenando modelo campeón...")

model.fit(
    X,
    y
)

# =========================================================

# SAVE MODEL

# =========================================================

dump(
    model,
    MODEL_FILE
)

print(
    f"\nModelo guardado en:\n"
    f"{MODEL_FILE}"
)

# =========================================================

# COPY FEATURES

# =========================================================

copyfile(
    TOP30_FILE,
    CHAMPION_DIR / "top30_features.csv"
)

print(
    "\nTop30 copiada."
)

# =========================================================

# METADATA

# =========================================================

metadata = {
    "version": "v1.0_model_champion",
    "created_at": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "model": "Stacking Ensemble",
    "features_used": len(features),
    "dataset_rows": int(len(X)),
    "dataset_timestamp": dataset_modified,
    "holdout_f1_macro": 0.4915,
    "cross_validation_f1_macro": 0.4810,
    "accuracy": 0.5123
}

with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )


print(
    "\nMetadata guardada."
)

# =========================================================

# README

# =========================================================

readme_text = """

    # v1.0_model_champion

    Modelo oficial del proyecto.

    ## Arquitectura

    Stacking Ensemble

    ### Base Models

    * Random Forest Tuned
    * Logistic Regression

    ### Meta Model

    * Logistic Regression

    ## Features

    Top30 seleccionadas mediante Feature Importance.

    ## Resultados

    Accuracy: 0.5123

    Holdout F1 Macro: 0.4915

    Cross Validation F1 Macro: 0.4810

    ## Dataset

    training_dataset.parquet

    Observaciones: 12,599

    ## Fecha

    2026-06-22
    """

with open(
    README_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        readme_text.strip()
    )


print(
    "\nREADME generado."
)

print("\n" + "=" * 60)
print("MODELO CAMPEÓN EXPORTADO")
print("=" * 60)

print(
    f"\nUbicación:\n{CHAMPION_DIR}"
)
