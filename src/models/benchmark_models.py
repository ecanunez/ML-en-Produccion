import time
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

from load_dataset import load_dataset
from evaluate_models import evaluate_model
from log_experiment import log_experiment


# =========================================================
# 1. CARGA DATASET
# =========================================================

X, y, features = load_dataset()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================================================
# 2. MODELOS
# =========================================================

models = {
    "Baseline_Dummy": DummyClassifier(strategy="most_frequent"),

    "LogReg": LogisticRegression(
        max_iter=5000,
        class_weight="balanced"
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
# 3. BENCHMARK LOOP
# =========================================================

results = []

for name, model in models.items():

    print("\n" + "=" * 60)
    print(f"Entrenando: {name}")
    print("=" * 60)

    start = time.time()

    model.fit(X_train, y_train)

    train_time = time.time() - start

    # OJO: tu función retorna (accuracy, f1_macro)
    accuracy, f1_macro = evaluate_model(
        model,
        X_test,
        y_test,
        model_name=name
    )

    result = {
        "model": name,
        "accuracy": accuracy,
        "f1_macro": f1_macro,
        "train_time_sec": round(train_time, 4)
    }

    results.append(result)

    log_experiment(name, result)


# =========================================================
# 4. RESULTADOS
# =========================================================

df = pd.DataFrame(results)

df = df.sort_values(
    by="f1_macro",
    ascending=False
)

print("\n" + "=" * 60)
print("BENCHMARK FINAL")
print("=" * 60)
print(df)


# =========================================================
# 5. GUARDAR
# =========================================================

df.to_csv(
    "src/reports/benchmark_results.csv",
    index=False
)

print("\nGuardado en src/reports/benchmark_results.csv")