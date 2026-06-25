from pathlib import Path

import pandas as pd
from joblib import load

from src.config.project_config import (
    MODEL_VERSION
)

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = (
    ROOT
    / "models"
    / "champions"
    / MODEL_VERSION
)

MODEL_FILE = MODEL_DIR / "model.joblib"

FEATURES_FILE = (
    MODEL_DIR
    / "top30_features.csv"
)

# =========================================================
# VALIDATION
# =========================================================

if not MODEL_FILE.exists():

    raise FileNotFoundError(
        f"No existe el modelo: {MODEL_FILE}"
    )

if not FEATURES_FILE.exists():

    raise FileNotFoundError(
        f"No existe el archivo de features: "
        f"{FEATURES_FILE}"
    )

# =========================================================
# LOAD MODEL
# =========================================================

MODEL = load(MODEL_FILE)

MODEL_FEATURES = (
    pd.read_csv(
        FEATURES_FILE
    )["feature"].tolist()
)

print(
    f"Modelo cargado: "
    f"{MODEL_FILE.name}"
)

print(
    f"Features esperadas: "
    f"{len(MODEL_FEATURES)}"
)

# =========================================================
# PREDICT FUNCTION
# =========================================================

def predict_matches(df):

    missing = [
        col
        for col in MODEL_FEATURES
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Faltan columnas requeridas: "
            f"{missing}"
        )

    X = df[MODEL_FEATURES]

    predictions = MODEL.predict(X)

    probabilities = (
        MODEL.predict_proba(X)
    )

    results = df.copy()

    results["prediction"] = (
        predictions
    )

    results["prob_away"] = (
        probabilities[:, 0]
    )

    results["prob_draw"] = (
        probabilities[:, 1]
    )

    results["prob_home"] = (
        probabilities[:, 2]
    )

    return results

# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_file = (
        ROOT
        / "data"
        / "processed"
        / "training_dataset.parquet"
    )

    df = pd.read_parquet(
        sample_file
    )

    predictions = (
        predict_matches(
            df.head(5)
        )
    )

    print(
        predictions[
            [
                "prediction",
                "prob_away",
                "prob_draw",
                "prob_home"
            ]
        ]
    )