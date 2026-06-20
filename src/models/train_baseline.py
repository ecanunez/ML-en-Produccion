from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from evaluate_model import evaluate_model
from src.reports.log_experiment import log_experiment

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT
    / "data"
    / "processed"
    / "training_dataset.parquet"
)

def main():

    print("Leyendo dataset...")

    df = pd.read_parquet(
        DATA_FILE
    )

    print(
        f"Observaciones originales: "
        f"{len(df):,}"
    )

    df = df[
        df["target"].notna()
    ].copy()

    print(
        f"Observaciones finales: "
        f"{len(df):,}"
    )

    features = [
        c
        for c in df.columns
        if c not in [
            "match_idx",
            "target",
            "home_elo",
            "away_elo",
            "home_team_market_value_mean",
            "away_team_market_value_mean",
            "home_GK_market_value_mean",
            "away_GK_market_value_mean"
        ]
    ]

    print(
        f"Features utilizadas: "
        f"{len(features)}"
    )

    X = df[features]

    y = df["target"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
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
                random_state=42
            )
        )
    ])

    logreg.fit(
        X_train,
        y_train
    )

    acc_logreg, f1_logreg = evaluate_model(
        logreg,
        X_test,
        y_test,
        "LOGISTIC REGRESSION"
    )

    log_experiment(
        dataset="training_dataset_fe_v1",
        model="LogisticRegression",
        f1_macro=f1_logreg,
        accuracy=acc_logreg,
        features=X.shape[1],
        train_rows=len(X),
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
        random_state=42,
        n_jobs=-1
    )

    rf.fit(
        X_train,
        y_train
    )

    acc_rf, f1_rf = evaluate_model(
        rf,
        X_test,
        y_test,
        "RANDOM FOREST"
    )

    log_experiment(
        dataset="training_dataset_v1",
        model="RandomForest",
        f1_macro=f1_rf,
        accuracy=acc_rf,
        features=X.shape[1],
        train_rows=len(X),
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
