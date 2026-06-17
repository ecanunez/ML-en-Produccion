from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)


ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT
    / "data"
    / "processed"
    / "training_dataset.parquet"
)


def evaluate_model(
    model,
    X_test,
    y_test,
    model_name
):

    preds = model.predict(X_test)

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    print(
        f"Accuracy: "
        f"{accuracy_score(y_test, preds):.4f}"
    )

    print(
        f"F1 Macro: "
        f"{f1_score(y_test, preds, average='macro'):.4f}"
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


def main():

    print("Leyendo dataset...")

    df = pd.read_parquet(
        DATA_FILE
    )

    print(
        f"Observaciones: {len(df):,}"
    )

    features = [
        "home_players_found",
        "away_players_found",
        "home_team_market_value",
        "away_team_market_value",
        "market_value_diff"
    ]

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

    # -----------------------------------
    # Logistic Regression
    # -----------------------------------

    logreg = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=2000,
                random_state=42
            )
        )
    ])

    logreg.fit(
        X_train,
        y_train
    )

    evaluate_model(
        logreg,
        X_test,
        y_test,
        "LOGISTIC REGRESSION"
    )

    # -----------------------------------
    # Random Forest
    # -----------------------------------

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    rf.fit(
        X_train,
        y_train
    )

    evaluate_model(
        rf,
        X_test,
        y_test,
        "RANDOM FOREST"
    )

    # -----------------------------------
    # Feature Importance
    # -----------------------------------

    importance = pd.DataFrame({
        "feature": features,
        "importance": rf.feature_importances_
    })

    importance = importance.sort_values(
        "importance",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)

    print(
        importance.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()