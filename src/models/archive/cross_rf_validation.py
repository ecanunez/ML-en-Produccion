from pathlib import Path
import time
import pandas as pd
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from load_dataset import load_dataset
from src.config.project_config import (
    RANDOM_STATE
)


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
    / "cross_validation_results.csv"
)


# =========================================================
# DATASET
# =========================================================

X, y, features, dataset_modified = load_dataset()

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

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
    random_state=RANDOM_STATE
)


# =========================================================
# MODELOS
# =========================================================

models = {

    "LogisticRegression": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            )
        )
    ]),

    "RandomForest_Tuned": RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    ),

    "XGBoost": XGBClassifier(
        objective="multi:softprob",
        num_class=3,
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE
    ),

    "LightGBM": LGBMClassifier(
        objective="multiclass",
        num_class=3,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=RANDOM_STATE,
        verbose=-1
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

    if model_name in ["XGBoost", "LightGBM"]:

        start = time.time()
        scores = cross_val_score(
            estimator=model,
            X=X,
            y=y_encoded,
            cv=cv,
            scoring="f1_macro",
            n_jobs=-1
        )
        elapsed = time.time() - start
        print(
            f"Tiempo: "
            f"{elapsed:.1f} seg"
        )

    else:
        start = time.time()
        scores = cross_val_score(
            estimator=model,
            X=X,
            y=y,
            cv=cv,
            scoring="f1_macro",
            n_jobs=-1
        )
        elapsed = time.time() - start
        print(
            f"Tiempo: "
            f"{elapsed:.1f} seg"
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
        ),
        "cv_time_sec": round(elapsed, 2)
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