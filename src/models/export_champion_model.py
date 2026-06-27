from pathlib import Path

import joblib

from src.models.train import train_model


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


def main():

    print("\n" + "=" * 60)
    print("EXPORT CHAMPION MODEL")
    print("=" * 60)

    artifact = train_model()

    joblib.dump(
        artifact,
        MODEL_FILE
    )

    print("\nModelo exportado en:")
    print(MODEL_FILE)

    print("\nMétricas:")

    for key, value in artifact["metrics"].items():

        if isinstance(value, (int, float)):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()