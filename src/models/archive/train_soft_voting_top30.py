import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestClassifier,
    VotingClassifier
)
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.models.load_dataset import load_dataset
from src.config.project_config import RANDOM_STATE, REPORTS_DIR

# =========================================================

# FEATURES

# =========================================================

TOP30_FILE = REPORTS_DIR / "top30_features.csv"

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

print(f"Features utilizadas: {len(features)}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
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
    random_state=RANDOM_STATE,
    n_jobs=-1
)

lgbm = LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    random_state=RANDOM_STATE,
    verbose=-1
)

xgb = XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=RANDOM_STATE,
    eval_metric="mlogloss"
)

# =========================================================

# ENSEMBLE

# =========================================================

model = VotingClassifier(
    estimators=[
    ("rf", rf),
    ("lgbm", lgbm),
    ("xgb", xgb)
    ],
    voting="soft",
    n_jobs=-1
)

# =========================================================

# TRAIN

# =========================================================

print("Entrenando Soft Voting Ensemble...")

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
print("SOFT VOTING ENSEMBLE")
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
