from pathlib import Path

import pandas as pd
from joblib import load

from src.config.project_config import MODEL_VERSION

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

# =========================================================
# VALIDATION
# =========================================================

if not MODEL_FILE.exists():

    raise FileNotFoundError(
        f"No existe el modelo: {MODEL_FILE}"
    )

# =========================================================
# LOAD ARTIFACT
# =========================================================

artifact = load(MODEL_FILE)

MODEL = artifact.get("model")

MODEL_FEATURES = artifact.get("features", [])

MODEL_NAME = artifact.get(
    "model_name",
    "unknown"
)

FEATURE_SET = artifact.get(
    "feature_set",
    "unknown"
)

METRICS = artifact.get(
    "metrics",
    {}
)

VERSION = artifact.get(
    "version",
    "unknown"
)

DATASET_ROWS = artifact.get(
    "dataset_rows",
    None
)

DATASET_TIMESTAMP = artifact.get(
    "dataset_timestamp",
    None
)

# =========================================================
# INFO
# =========================================================

print("\n" + "=" * 60)
print("CHAMPION MODEL LOADED")
print("=" * 60)

print(f"Version      : {VERSION}")
print(f"Model        : {MODEL_NAME}")
print(f"Feature set  : {FEATURE_SET}")
print(f"N Features   : {len(MODEL_FEATURES)}")

if METRICS:

    print()

    for metric, value in METRICS.items():

        print(
            f"{metric}: {value:.4f}"
        )

print("=" * 60)

# =========================================================
# PREDICT
# =========================================================

def predict_matches(df):

    missing = [
        feature
        for feature in MODEL_FEATURES
        if feature not in df.columns
    ]

    if missing:

        raise ValueError(
            "Faltan columnas requeridas:\n"
            + "\n".join(missing)
        )

    X = df[
        MODEL_FEATURES
    ]

    predictions = MODEL.predict(X)

    probabilities = MODEL.predict_proba(X)

    results = df.copy()

    results["prediction"] = predictions

    results["prob_away"] = probabilities[:, 0]

    results["prob_draw"] = probabilities[:, 1]

    results["prob_home"] = probabilities[:, 2]

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

    predictions = predict_matches(
        df.head(5)
    )

    print()

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