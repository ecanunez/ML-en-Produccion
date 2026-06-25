from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)
from load_dataset import load_dataset
from src.config.project_config import (
    RANDOM_STATE
)

# =========================================================

# CONFIG

# =========================================================

ROOT = Path(__file__).resolve().parents[2]

TOP30_FILE = (
    ROOT
    / "src"
    / "reports"
    / "top30_features.csv"
)

# =========================================================

# FEATURES

# =========================================================

top30_features = (
    pd.read_csv(TOP30_FILE)["feature"]
    .tolist()
)

# =========================================================

# DATASET

# =========================================================

X, y, features, dataset_modified = load_dataset(
    selected_features=top30_features
)

print(
    f"Features utilizadas: "
    f"{len(features)}"
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

# =========================================================

# RANDOM FOREST BASE

# =========================================================

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

# =========================================================

# CALIBRATION

# =========================================================

model = CalibratedClassifierCV(
    estimator=rf,
    method="isotonic",
    cv=5
)

# =========================================================

# TRAIN

# =========================================================

print("Entrenando Random Forest Calibrated...")

model.fit(
    X_train,
    y_train
)

preds = model.predict(
    X_test
)

# =========================================================

# METRICS

# =========================================================

accuracy = accuracy_score(
    y_test,
    preds
)

f1 = f1_score(
    y_test,
    preds,
    average="macro"
)

precision = precision_score(
    y_test,
    preds,
    average="macro"
)

recall = recall_score(
    y_test,
    preds,
    average="macro"
)

print("\n" + "=" * 60)
print("RANDOM FOREST CALIBRATED TOP30")
print("=" * 60)

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"F1 Macro: {f1:.4f}"
)

print(
    f"Precision Macro: {precision:.4f}"
)

print(
    f"Recall Macro: {recall:.4f}"
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        preds
    )
)

print("\nClassification Report")

print(
    classification_report(
        y_test,
        preds,
        digits=4
    )
)
