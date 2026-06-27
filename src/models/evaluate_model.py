import argparse

from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestClassifier,
    StackingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.config.project_config import RANDOM_STATE
from src.config.feature_registry import load_feature_set
from src.models.load_dataset import load_dataset
from src.models.evaluate_model import evaluate_model


# =========================================================
# MODEL FACTORY
# =========================================================

def get_model(name: str):

    if name == "rf":
        return RandomForestClassifier(
            n_estimators=500,
            max_depth=10,
            min_samples_leaf=5,
            min_samples_split=2,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

    if name == "xgb":
        return XGBClassifier(
            eval_metric="mlogloss",
            random_state=RANDOM_STATE
        )

    if name == "lgbm":
        return LGBMClassifier(
            random_state=RANDOM_STATE
        )

    if name == "stacking":

        rf = RandomForestClassifier(
            n_estimators=500,
            max_depth=10,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

        lr = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            ))
        ])

        return StackingClassifier(
            estimators=[
                ("rf", rf),
                ("lr", lr)
            ],
            final_estimator=LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            ),
            stack_method="predict_proba",
            cv=5,
            n_jobs=-1
        )

    raise ValueError(f"Modelo no soportado: {name}")


# =========================================================
# TRAIN PIPELINE
# =========================================================

def run_training(model_name: str, feature_set: str):

    # FEATURES
    features = load_feature_set(feature_set)

    # DATASET
    X, y, _, _ = load_dataset(selected_features=features)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # MODEL
    model = get_model(model_name)

    print("\n" + "=" * 60)
    print(f"MODELO: {model_name}")
    print(f"FEATURE SET: {feature_set}")
    print("=" * 60)

    # TRAIN
    model.fit(X_train, y_train)

    # EVALUATION (centralizada)
    metrics = evaluate_model(
        model=model,
        X_test=X_test,
        y_test=y_test,
        model_name=model_name,
        verbose=True
    )

    return model, metrics


# =========================================================
# CLI ENTRYPOINT
# =========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        default="rf",
        choices=["rf", "xgb", "lgbm", "stacking"]
    )

    parser.add_argument(
        "--features",
        default="top30"
    )

    args = parser.parse_args()

    run_training(
        model_name=args.model,
        feature_set=args.features
    )