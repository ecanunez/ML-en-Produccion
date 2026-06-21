import time
from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    HistGradientBoostingClassifier
)

from load_dataset import load_dataset
from evaluate_model import evaluate_model


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
    / "benchmark_results.csv"
)


# =========================================================
# CARGA DEL DATASET
# =========================================================

X, y, features = load_dataset()

print(
    f"\nTotal de features: "
    f"{len(features)}"
)

print(
    f"Total observaciones: "
    f"{len(X):,}"
)

print(
    f"Valores faltantes: "
    f"{X.isna().sum().sum():,}"
)


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(
    f"\nTrain: {len(X_train):,}"
)

print(
    f"Test: {len(X_test):,}"
)


# =========================================================
# MODELOS
# =========================================================

models = {
    "Baseline_Dummy": DummyClassifier(
        strategy="most_frequent"
    ),

    "LogisticRegression": LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=42
    ),

    "RandomForest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "RandomForest_Tuned": RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "HistGradientBoosting": HistGradientBoostingClassifier(
        random_state=42
    )
}


# =========================================================
# BENCHMARK
# =========================================================

results = []

for model_name, model in models.items():

    print("\n")
    print("=" * 60)
    print(f"ENTRENANDO: {model_name}")
    print("=" * 60)

    start_time = time.time()

    model.fit(
        X_train,
        y_train
    )

    train_time = time.time() - start_time

    metrics = evaluate_model(
        model=model,
        X_test=X_test,
        y_test=y_test,
        model_name=model_name
    )

    results.append(
        {
            "model": model_name,
            "accuracy": round(
                metrics["accuracy"],
                4
            ),
            "f1_macro": round(
                metrics["f1_macro"],
                4
            ),
            "precision_macro": round(
                metrics["precision_macro"],
                4
            ),
            "recall_macro": round(
                metrics["recall_macro"],
                4
            ),
            "train_time_sec": round(
                train_time,
                2
            )
        }
    )


# =========================================================
# RESULTADOS
# =========================================================

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    by="f1_macro",
    ascending=False
)

results_df = results_df.reset_index(
    drop=True
)

results_df.index += 1

print("\n")
print("=" * 60)
print("BENCHMARK FINAL")
print("=" * 60)

print(results_df)


# =========================================================
# EXPORTAR CSV
# =========================================================

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nResultados guardados en:\n"
    f"{OUTPUT_FILE}"
)