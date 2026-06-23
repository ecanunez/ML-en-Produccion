from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import (
    RandomForestClassifier,
    StackingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

from load_dataset import load_dataset

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
    random_state=42,
    stratify=y
)

# =========================================================

# BASE MODELS

# =========================================================

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

lr = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)

# =========================================================

# STACKING

# =========================================================

model = StackingClassifier(
    estimators=[
        ("rf", rf),
        ("lr", lr)
    ],
    final_estimator=LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=42
    ),
    stack_method="predict_proba",
    cv=5,
    n_jobs=-1
)

# =========================================================

# TRAIN

# =========================================================

print(
    "Entrenando Stacking Ensemble..."
)

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
print("STACKING ENSEMBLE")
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
