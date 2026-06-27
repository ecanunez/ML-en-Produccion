from pathlib import Path

import joblib

from src.models.train import run_training
from src.config.experiment_config import (
    CHAMPION_MODEL,
    CHAMPION_FEATURE_SET
)
from src.config.project_config import (
    MODEL_VERSION,
)
from src.config.feature_sets import (
    load_feature_set
)

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_FILE = (
    MODEL_DIR
    / "champion_model.pkl"
)

# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n" + "=" * 60)
    print("EXPORT CHAMPION MODEL")
    print("=" * 60)

    print(f"Modelo: {CHAMPION_MODEL}")
    print(f"Feature Set: {CHAMPION_FEATURE_SET}")

    features = load_feature_set(
        CHAMPION_FEATURE_SET
    )

    model, metrics = run_training(
        model_name=CHAMPION_MODEL,
        features=features
    )

    artifact = {
        "model": model,
        "model_name": CHAMPION_MODEL,
        "feature_set": CHAMPION_FEATURE_SET,
        "features": features,
        "metrics": metrics,
        "version": MODEL_VERSION
    }

    joblib.dump(
        artifact,
        MODEL_FILE
    )

    print("\nModelo exportado en:")
    print(MODEL_FILE)

    print("\nMétricas:")

    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":
    main()