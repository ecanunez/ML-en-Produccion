from pathlib import Path

import pandas as pd

from joblib import load


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = (
    ROOT
    / "models"
    / "champions"
    / "v1.0_model_champion"
)

MODEL_FILE = (
    MODEL_DIR
    / "model.joblib"
)

FEATURES_FILE = (
    MODEL_DIR
    / "top30_features.csv"
)


# =========================================================
# LOAD MODEL
# =========================================================

model = load(MODEL_FILE)

top30_features = (
    pd.read_csv(FEATURES_FILE)["feature"]
    .tolist()
)

print(
    f"Modelo cargado: {MODEL_FILE.name}"
)

print(
    f"Features esperadas: {len(top30_features)}"
)


# =========================================================
# PREDICT FUNCTION
# =========================================================

def predict_matches(df):

    missing = [
        col
        for col in top30_features
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Faltan columnas: {missing}"
        )

    X = df[top30_features]

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)

    results = df.copy()

    results["prediction"] = predictions

    results["prob_away"] = probabilities[:, 0]
    results["prob_draw"] = probabilities[:, 1]
    results["prob_home"] = probabilities[:, 2]

    return results

if __name__ == "__main__":

    sample_file = (
        ROOT
        / "data"
        / "processed"
        / "training_dataset.parquet"
    )

    df = pd.read_parquet(sample_file)

    predictions = predict_matches(
        df.head(5)
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