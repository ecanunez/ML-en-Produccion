from pathlib import Path
from datetime import datetime

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from load_dataset import load_dataset


ROOT = Path(__file__).resolve().parents[2]

IMPORTANCE_FILE = (
    ROOT / "src" / "reports" / "feature_importance_rf_v2.csv"
)

OUTPUT_FILE = (
    ROOT / "src" / "reports" / "feature_selection_results.csv"
)

TOP30_OUTPUT = (
    ROOT / "src" / "reports" / "top30_features.csv"
)

TOP40_OUTPUT = (
    ROOT / "src" / "reports" / "top40_features.csv"
)

TOP50_OUTPUT = (
    ROOT / "src" / "reports" / "top50_features.csv"
)

ARCHIVE_DIR = (
    ROOT / "src" / "reports" / "archive"
)


# ------------------------------------------------------------
# MODEL EVALUATION
# ------------------------------------------------------------
def evaluate_feature_set(feature_list):

    X, y, _, _ = load_dataset(
        selected_features=feature_list
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    return f1_score(
        y_test,
        preds,
        average="macro"
    )


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():

    ARCHIVE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 60)
    print("FEATURE SELECTION EXPERIMENT")
    print("=" * 60)

    importance = pd.read_csv(
        IMPORTANCE_FILE
    )

    importance = (
        importance
        .sort_values(
            "importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ------------------------------------------------------------
    # TOP FEATURES
    # ------------------------------------------------------------
    top30_features = (
        importance
        .head(30)["feature"]
        .tolist()
    )

    top40_features = (
        importance
        .head(40)["feature"]
        .tolist()
    )

    top50_features = (
        importance
        .head(50)["feature"]
        .tolist()
    )

    pd.DataFrame(
        {"feature": top30_features}
    ).to_csv(
        TOP30_OUTPUT,
        index=False
    )

    pd.DataFrame(
        {"feature": top40_features}
    ).to_csv(
        TOP40_OUTPUT,
        index=False
    )

    pd.DataFrame(
        {"feature": top50_features}
    ).to_csv(
        TOP50_OUTPUT,
        index=False
    )

    print(
        f"\nTop30 guardadas en:\n{TOP30_OUTPUT}"
    )

    print(
        f"\nTop40 guardadas en:\n{TOP40_OUTPUT}"
    )

    print(
        f"\nTop50 guardadas en:\n{TOP50_OUTPUT}"
    )

    # ------------------------------------------------------------
    # EXPERIMENTS
    # ------------------------------------------------------------
    experiments = {
        "Top10": importance.head(10)["feature"].tolist(),
        "Top20": importance.head(20)["feature"].tolist(),
        "Top30": top30_features,
        "Top40": top40_features,
        "Top50": top50_features,
        "Top60": importance.head(60)["feature"].tolist(),
        "All": importance["feature"].tolist()
    }

    results = []

    for name, features in experiments.items():

        print("\n" + "-" * 60)
        print(name)
        print(f"Features: {len(features)}")

        f1 = evaluate_feature_set(
            features
        )

        print(
            f"F1 Macro: {f1:.4f}"
        )

        results.append({
            "experiment": name,
            "n_features": len(features),
            "f1_macro": round(f1, 4)
        })

    # ------------------------------------------------------------
    # RESULTS
    # ------------------------------------------------------------
    results_df = pd.DataFrame(
        results
    )

    results_df = (
        results_df
        .sort_values(
            "f1_macro",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)

    print(results_df)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nResultados guardados en:"
    )

    print(
        OUTPUT_FILE
    )

    # ------------------------------------------------------------
    # ARCHIVE
    # ------------------------------------------------------------
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    archive_results = (
        ARCHIVE_DIR
        / f"feature_selection_results_{timestamp}.csv"
    )

    archive_top30 = (
        ARCHIVE_DIR
        / f"top30_features_{timestamp}.csv"
    )

    archive_top40 = (
        ARCHIVE_DIR
        / f"top40_features_{timestamp}.csv"
    )

    archive_top50 = (
        ARCHIVE_DIR
        / f"top50_features_{timestamp}.csv"
    )

    archive_importance = (
        ARCHIVE_DIR
        / f"feature_importance_{timestamp}.csv"
    )

    results_df.to_csv(
        archive_results,
        index=False
    )

    pd.DataFrame(
        {"feature": top30_features}
    ).to_csv(
        archive_top30,
        index=False
    )

    pd.DataFrame(
        {"feature": top40_features}
    ).to_csv(
        archive_top40,
        index=False
    )

    archive_top50 = (
        ARCHIVE_DIR
        / f"top50_features_{timestamp}.csv"
    )


    importance.to_csv(
        archive_importance,
        index=False
    )

    print("\nBackups generados:")

    print(archive_results)
    print(archive_top30)
    print(archive_top40)
    print(archive_top50)
    print(archive_importance)


if __name__ == "__main__":
    main()