from pathlib import Path
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from load_alt2_dataset import load_dataset


ROOT = Path(__file__).resolve().parents[2]

IMPORTANCE_FILE = (
    ROOT / "src" / "reports" / "feature_importance_rf_v2.csv"
)

OUTPUT_FILE = (
    ROOT / "src" / "reports" / "feature_selection_results.csv"
)

TOP40_OUTPUT = (
    ROOT / "src" / "reports" / "top40_features.csv"
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

    print("\n" + "=" * 60)
    print("FEATURE SELECTION EXPERIMENT")
    print("=" * 60)

    importance = pd.read_csv(IMPORTANCE_FILE)

    # Ordenar por importancia por seguridad
    importance = importance.sort_values(
        "importance",
        ascending=False
    ).reset_index(drop=True)

    # ------------------------------------------------------------
    # Generar Top40 automáticamente
    # ------------------------------------------------------------
    top40_features = importance.head(40)["feature"].tolist()

    pd.DataFrame(
        {"feature": top40_features}
    ).to_csv(
        TOP40_OUTPUT,
        index=False
    )

    print(f"\nTop40 guardadas en:\n{TOP40_OUTPUT}")

    # ------------------------------------------------------------
    # Experimentos
    # ------------------------------------------------------------
    experiments = {
        "Top10": importance.head(10)["feature"].tolist(),
        "Top20": importance.head(20)["feature"].tolist(),
        "Top30": importance.head(30)["feature"].tolist(),
        "Top40": top40_features,
        "Top50": importance.head(50)["feature"].tolist(),
        "All": importance["feature"].tolist()
    }

    results = []

    for name, features in experiments.items():

        print("\n" + "-" * 60)
        print(name)
        print(f"Features: {len(features)}")

        f1 = evaluate_feature_set(features)

        print(f"F1 Macro: {f1:.4f}")

        results.append({
            "experiment": name,
            "n_features": len(features),
            "f1_macro": round(f1, 4)
        })

    # ------------------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------------------
    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "f1_macro",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)

    print(results_df)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nResultados guardados en:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()