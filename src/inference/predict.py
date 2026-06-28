from pathlib import Path

import pandas as pd
from joblib import load

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    ROOT
    / "models"
    / "champion_model.pkl"
)

SCORING_DATASET_FILE = (
    ROOT
    / "data"
    / "processed"
    / "scoring_dataset.parquet"
)

PREDICTIONS_FILE = (
    ROOT
    / "data"
    / "processed"
    / "predictions.csv"
)

# =========================================================
# VALIDATION
# =========================================================

if not MODEL_FILE.exists():

    raise FileNotFoundError(
        f"No existe el modelo: {MODEL_FILE}"
    )

if not SCORING_DATASET_FILE.exists():

    raise FileNotFoundError(
        f"No existe el scoring dataset: {SCORING_DATASET_FILE}"
    )

# =========================================================
# LOAD ARTIFACT
# =========================================================

artifact = load(
    MODEL_FILE
)

MODEL = artifact["model"]

MODEL_FEATURES = artifact["features"]

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

        if isinstance(value, (int, float)):
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value}")

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

    predictions = MODEL.predict(
        X
    )

    probabilities = MODEL.predict_proba(
        X
    )

    results = df.copy()

    results["prediction"] = predictions

    results["prob_away"] = probabilities[:, 0]
    results["prob_draw"] = probabilities[:, 1]
    results["prob_home"] = probabilities[:, 2]

    return results


# =========================================================
# MAIN
# =========================================================

def main():

    df = pd.read_parquet(
        SCORING_DATASET_FILE
    )

    predictions = predict_matches(
        df
    )

    predictions.to_csv(
        PREDICTIONS_FILE,
        index=False
    )

    print("\nPredicciones generadas:")
    print(PREDICTIONS_FILE)

    print("\nPreview:")

    print(
        predictions[
            [
                "home_team",
                "away_team",
                "prediction",
                "prob_away",
                "prob_draw",
                "prob_home"
            ]
        ].head()
    )


if __name__ == "__main__":

    main()