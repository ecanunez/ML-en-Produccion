from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from load_dataset import load_dataset
from evaluate_model import evaluate_model
from log_experiment import log_experiment

X, y, features = load_dataset()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

acc, f1 = evaluate_model(
    rf,
    X_test,
    y_test,
    "RANDOM FOREST TUNED"
)

importance = pd.DataFrame({
    "feature": features,
    "importance": rf.feature_importances_
})

importance = (
    importance
    .sort_values("importance", ascending=False)
)

print("\nTOP 20 FEATURES")
print(importance.head(20))

importance.to_csv(
    "src/reports/feature_importance_rf_v2.csv",
    index=False
)

log_experiment(
    dataset="training_dataset.parquet",
    model="RandomForestTuned",
    f1_macro=f1,
    accuracy=acc,
    features=X.shape[1],
    train_rows=len(X),
    params=(
        "n_estimators=500,"
        "max_depth=10,"
        "min_samples_leaf=5,"
        "min_samples_split=2,"
        "class_weight=balanced"
    ),
    notes="Feature Engineering v1"
)