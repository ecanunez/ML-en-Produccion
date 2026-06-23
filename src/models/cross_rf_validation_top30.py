from pathlib import Path

import pandas as pd

from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from load_dataset import load_dataset


# =========================================================
# CONFIGURACIÓN
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

REPORTS_DIR = (
    ROOT
    / "src"
    / "reports"
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    REPORTS_DIR
    / "cross_validation_results_top30.csv"
)

# =========================================================
# DATASET
# =========================================================

TOP30_FILE = (
    ROOT
    / "src"
    / "reports"
    / "top30_features.csv"
)

top30_features = (
    pd.read_csv(TOP30_FILE)["feature"]
    .tolist()
)

X, y, features, dataset_modified = load_dataset(
    selected_features=top30_features
)

print(
    f"\nDataset modificado: "
    f"{dataset_modified}"
)

print(
    f"Observaciones: "
    f"{len(X):,}"
)

print(
    f"Features: "
    f"{len(features)}"
)

# =========================================================
# CROSS VALIDATION
# =========================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# =========================================================
# MODELOS
# =========================================================

models = {

    "RandomForest_Tuned_Top30": RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

}

# =========================================================
# VALIDACIÓN CRUZADA
# =========================================================

results = []

for model_name, model in models.items():

    print("\n")
    print("=" * 60)
    print(model_name)
    print("=" * 60)

    scores = cross_val_score(
        estimator=model,
        X=X,
        y=y,
        cv=cv,
        scoring="f1_macro",
        n_jobs=-1
    )

    print("\nFold scores:")

    for i, score in enumerate(scores, start=1):

        print(
            f"Fold {i}: "
            f"{score:.4f}"
        )

    mean_score = scores.mean()
    std_score = scores.std()

    print(
        f"\nMean F1 Macro: "
        f"{mean_score:.4f}"
    )

    print(
        f"Std: "
        f"{std_score:.4f}"
    )

    print(
        f"Min: "
        f"{scores.min():.4f}"
    )

    print(
        f"Max: "
        f"{scores.max():.4f}"
    )

    results.append({
        "model": model_name,
        "n_features": len(features),
        "mean_f1_macro": round(
            mean_score,
            4
        ),
        "std_f1_macro": round(
            std_score,
            4
        ),
        "min_f1_macro": round(
            scores.min(),
            4
        ),
        "max_f1_macro": round(
            scores.max(),
            4
        )
    })

# =========================================================
# EXPORTAR RESULTADOS
# =========================================================

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    by="mean_f1_macro",
    ascending=False
)

print("\n")
print("=" * 60)
print("RESULTADOS FINALES")
print("=" * 60)

print(results_df)

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nResultados guardados en:\n"
    f"{OUTPUT_FILE}"
)