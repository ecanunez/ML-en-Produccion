from sklearn.model_selection import train_test_split

from src.config.project_config import RANDOM_STATE
from src.config.experiment_config import (
    MODEL_NAME,
    FEATURE_SET
)

from src.config.feature_sets import load_feature_set

from src.models.load_dataset import load_dataset
from src.models.model_registry import get_model
from src.models.evaluate_model import evaluate_model


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():
    """
    Entrena el modelo definido en experiment_config.py
    y devuelve toda la información necesaria para
    exportar el modelo campeón.
    """

    # -----------------------------------------------------
    # FEATURE SET
    # -----------------------------------------------------

    features = load_feature_set(
        FEATURE_SET
    )

    # -----------------------------------------------------
    # DATASET
    # -----------------------------------------------------

    X, y, _, dataset_modified = load_dataset(
        selected_features=features
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # -----------------------------------------------------
    # MODEL
    # -----------------------------------------------------

    model = get_model(
        MODEL_NAME
    )

    print("\n" + "=" * 60)
    print("TRAINING")
    print("=" * 60)

    print(f"Modelo: {MODEL_NAME}")
    print(f"Feature set: {FEATURE_SET}")
    print(f"N features: {len(features)}")
    print(f"Observaciones: {len(X)}")

    # -----------------------------------------------------
    # FIT
    # -----------------------------------------------------

    model.fit(
        X_train,
        y_train
    )

    # -----------------------------------------------------
    # EVALUATION
    # -----------------------------------------------------

    metrics = evaluate_model(
        model=model,
        X_test=X_test,
        y_test=y_test,
        model_name=MODEL_NAME
    )

    print("\nEntrenamiento finalizado.")

    return {
        "model": model,
        "metrics": metrics,
        "features": features,
        "model_name": MODEL_NAME,
        "feature_set": FEATURE_SET,
        "dataset_rows": len(X),
        "dataset_timestamp": dataset_modified,
        "version": MODEL_VERSION,
        "random_state": RANDOM_STATE
    }

# =========================================================
# MAIN
# =========================================================

def main():

    train_model()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()