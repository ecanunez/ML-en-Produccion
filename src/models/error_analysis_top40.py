import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)
from sklearn.ensemble import RandomForestClassifier
from load_dataset import load_dataset
from evaluate_model import evaluate_model
from src.config.project_config import (
    RANDOM_STATE
)

# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("ERROR ANALYSIS TOP 40 FEATURES")
print("=" * 60)

X, y, features, dataset_modified = load_dataset()

top40 = pd.read_csv(
    "src/reports/top40_features.csv"
)

top40_features = (
    top40["feature"]
    .tolist()
)

X = X[top40_features]

features = top40_features

print(f"Observaciones: {len(X):,}")
print(f"Features utilizadas: {len(features)}")


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)


# ============================================================
# MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

print("\nEntrenando modelo...")

model.fit(
    X_train,
    y_train
)

y_pred = model.predict(X_test)


# ============================================================
# STANDARD EVALUATION
# ============================================================

metrics = evaluate_model(
    model,
    X_test,
    y_test,
    "RANDOM FOREST TUNED"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        digits=4
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

labels = ["HOME", "DRAW", "AWAY"]

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

print(cm_df)


# ============================================================
# ERROR ANALYSIS DATAFRAME
# ============================================================

analysis_df = X_test.copy()

analysis_df["real"] = y_test.values
analysis_df["pred"] = y_pred

analysis_df["correct"] = (
    analysis_df["real"]
    ==
    analysis_df["pred"]
)

analysis_df["error_type"] = (
    analysis_df["real"]
    +
    "_TO_"
    +
    analysis_df["pred"]
)


# ============================================================
# MOST COMMON ERRORS
# ============================================================

print("\n" + "=" * 60)
print("MOST COMMON ERRORS")
print("=" * 60)

print(
    analysis_df.loc[
        ~analysis_df["correct"],
        "error_type"
    ]
    .value_counts()
    .head(20)
)


# ============================================================
# SAVE FILES
# ============================================================

analysis_df.to_csv(
    "src/reports/error_analysis_top40_predictions.csv",
    index=False
)

cm_df.to_csv(
    "src/reports/confusion_matrix_top40.csv"
)

print("\nArchivos generados:")

print(
    "src/reports/error_analysis_predictions.csv"
)

print(
    "src/reports/confusion_matrix.csv"
)

print("\nProceso finalizado.")