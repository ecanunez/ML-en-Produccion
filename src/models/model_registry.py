from sklearn.ensemble import (
    RandomForestClassifier,
    VotingClassifier,
    StackingClassifier
)

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.config.project_config import RANDOM_STATE


# =========================================================
# FEATURE SELECTION MODELS
# =========================================================

def get_feature_selection_model():
    """
    Modelo usado para feature importance / selection.
    """
    return RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


# =========================================================
# BASE MODELS (TRAINING)
# =========================================================

def get_random_forest():
    return RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        min_samples_leaf=5,
        min_samples_split=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


def get_xgboost():
    return XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE,
        eval_metric="mlogloss"
    )


def get_lightgbm():
    return LGBMClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=RANDOM_STATE
    )


def get_logistic_regression():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=5000,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ))
    ])


# =========================================================
# ENSEMBLE MODELS
# =========================================================

def get_soft_voting():
    return VotingClassifier(
        estimators=[
            ("rf", get_random_forest()),
            ("xgb", get_xgboost()),
            ("lgbm", get_lightgbm())
        ],
        voting="soft",
        n_jobs=-1
    )


def get_stacking_champion():
    return StackingClassifier(
        estimators=[
            ("rf", get_random_forest()),
            ("lr", get_logistic_regression())
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


# =========================================================
# MODEL LOOKUP (OPTIONAL CLEAN INTERFACE)
# =========================================================

MODEL_REGISTRY = {
    "feature_selection": get_feature_selection_model,
    "random_forest": get_random_forest,
    "xgboost": get_xgboost,
    "lightgbm": get_lightgbm,
    "logistic_regression": get_logistic_regression,
    "soft_voting": get_soft_voting,
    "stacking_champion": get_stacking_champion
}


def get_model(name: str):
    """
    Devuelve un modelo por nombre.
    """
    if name not in MODEL_REGISTRY:
        raise ValueError(f"Modelo desconocido: {name}")

    return MODEL_REGISTRY[name]()