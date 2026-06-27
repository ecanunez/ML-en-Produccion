from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

from src.models.load_dataset import load_dataset
from src.config.project_config import RANDOM_STATE
from src.config.model_registry import get_model


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[3]

OUTPUT_FILE = (
    ROOT / "src" / "reports" / "feature_importance_ranking.csv"
)


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE PIPELINE")
    print("=" * 60)

    # -----------------------------------------------------
    # LOAD DATASET
    # -----------------------------------------------------

    X, y, feature_names, _ = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # -----------------------------------------------------
    # GET MODEL FROM REGISTRY
    # -----------------------------------------------------

    model = get_model("feature_importance")  
    model.fit(X_train, y_train)

    # -----------------------------------------------------
    # EXTRACT IMPORTANCE
    # -----------------------------------------------------

    if not hasattr(model, "feature_importances_"):
        raise ValueError(
            "El modelo no soporta feature_importances_"
        )

    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    })

    importance = (
        importance
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    importance.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nRanking guardado en:")
    print(OUTPUT_FILE)

    print("\nTop 10 features:")
    print(importance.head(10))


if __name__ == "__main__":
    main()