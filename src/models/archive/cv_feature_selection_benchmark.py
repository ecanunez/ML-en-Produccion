from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from load_alt2_dataset import load_dataset
from src.config.project_config import (
    RANDOM_STATE
)

ROOT = Path(__file__).resolve().parents[2]

IMPORTANCE_FILE = (
    ROOT / "src" / "reports" / "feature_importance_rf_v2.csv"
)


# ------------------------------------------------------------
# MODEL CONFIG
# ------------------------------------------------------------
def get_model():

    return RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


# ------------------------------------------------------------
# CV EVALUATION
# ------------------------------------------------------------
def evaluate_cv(features, n_splits=5):

    X, y, _, _ = load_dataset(
        selected_features=features
    )

    skf = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    scores = []

    for train_idx, val_idx in skf.split(X, y):

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = get_model()
        model.fit(X_train, y_train)

        preds = model.predict(X_val)

        f1 = f1_score(
            y_val,
            preds,
            average="macro"
        )

        scores.append(f1)

    return {
        "mean": np.mean(scores),
        "std": np.std(scores),
        "min": np.min(scores),
        "max": np.max(scores)
    }


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():

    print("\n" + "=" * 60)
    print("CV FEATURE SELECTION BENCHMARK")
    print("=" * 60)

    importance = pd.read_csv(IMPORTANCE_FILE)

    importance = importance.sort_values(
        "importance",
        ascending=False
    ).reset_index(drop=True)

    experiments = {
        "FULL": importance["feature"].tolist(),
        "TOP40": importance.head(40)["feature"].tolist(),
        "TOP30": importance.head(30)["feature"].tolist(),
    }

    results = []

    for name, features in experiments.items():

        print("\n" + "-" * 60)
        print(name)
        print(f"Features: {len(features)}")

        scores = evaluate_cv(features)

        print(
            f"F1 Macro: {scores['mean']:.4f} "
            f"(± {scores['std']:.4f})"
        )

        results.append({
            "model": name,
            "n_features": len(features),
            "mean_f1_macro": round(scores["mean"], 4),
            "std_f1_macro": round(scores["std"], 4),
            "min_f1_macro": round(scores["min"], 4),
            "max_f1_macro": round(scores["max"], 4),
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "mean_f1_macro",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("RESULTADOS CV")
    print("=" * 60)

    print(results_df)


    output_file = (
        ROOT / "src" / "reports" / "cv_feature_selection_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print("\nResultados guardados en:")
    print(output_file)


if __name__ == "__main__":
    main()