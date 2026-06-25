import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from load_dataset import load_dataset
from evaluate_model import evaluate_model
from log_experiment import log_experiment
from src.config.project_config import (
    RANDOM_STATE
)

def main():
    
    X, y, features = load_dataset()

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=RANDOM_STATE,
            stratify=y
        )
    )

    print(
        f"\nTrain: {len(X_train):,}"
    )

    print(
        f"Test: {len(X_test):,}"
    )

    # ==================================================
    # Logistic Regression
    # ==================================================

    logreg = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=3000,
                random_state=RANDOM_STATE
            )
        )
    ])

    logreg.fit(
        X_train,
        y_train
    )

    metrics_logreg = evaluate_model(
        logreg,
        X_test,
        y_test,
        "LOGISTIC REGRESSION"
    )

    log_experiment(
        dataset="training_dataset.parquet",
        dataset_modified=dataset_modified,
        model="LogisticRegression",
        f1_macro=metrics["f1_macro"],
        accuracy=metrics["accuracy"],
        precision_macro=metrics["precision_macro"],
        recall_macro=metrics["recall_macro"],
        features=X.shape[1],
        train_rows=len(X_train),
        params="max_iter=3000",
        notes="Baseline"
    )

    # ==================================================
    # Random Forest
    # ==================================================

    rf = RandomForestClassifier(
        n_estimators=500,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    rf.fit(
        X_train,
        y_train
    )

    metrics_rf = evaluate_model(
        rf,
        X_test,
        y_test,
        "RANDOM FOREST"
    )

    log_experiment(
        dataset="training_dataset.parquet",
        dataset_modified=dataset_modified,
        model="RandomForest",
        f1_macro=metrics["f1_macro"],
        accuracy=metrics["accuracy"],
        precision_macro=metrics["precision_macro"],
        recall_macro=metrics["recall_macro"],
        features=X.shape[1],
        train_rows=len(X_train),
        params=(
            "n_estimators=500,"
            "max_depth=12,"
            "min_samples_leaf=5,"
            "class_weight=balanced"
        ),
        notes="Baseline"
    )

    # ==================================================
    # Feature Importance
    # ==================================================

    importance = pd.DataFrame({
        "feature": features,
        "importance": rf.feature_importances_
    })

    importance = (
        importance
        .sort_values(
            "importance",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("TOP 30 FEATURE IMPORTANCE")
    print("=" * 60)

    importance.to_csv(
        "src/reports/feature_importance_baseline_rf.csv",
        index=False
    )

if __name__ == "__main__":
    main()
