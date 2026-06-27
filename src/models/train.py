from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

from src.config.project_config import RANDOM_STATE
from src.config.feature_sets import load_feature_set
from src.models.load_dataset import load_dataset
from src.models.model_registry import get_model
from src.models.evaluate_model import evaluate_model


def main(model_name: str, feature_set: str):

    # -------------------------
    # FEATURES
    # -------------------------
    features = load_feature_set(feature_set)

    # -------------------------
    # DATASET
    # -------------------------
    X, y, _, _ = load_dataset(selected_features=features)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # -------------------------
    # MODEL
    # -------------------------
    model = get_model(model_name)

    print("\n" + "=" * 60)
    print(f"Modelo: {model_name}")
    print(f"Feature set: {feature_set}")
    print(f"N features: {len(features) if features else 'ALL'}")
    print("=" * 60)

    model.fit(X_train, y_train)

    # -------------------------
    # EVALUATION CENTRALIZADA
    # -------------------------
    metrics = evaluate_model(
        model,
        X_test,
        y_test,
        model_name=model_name
    )

    return model, metrics


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--model", default="rf")
    parser.add_argument("--features", default="top30")

    args = parser.parse_args()

    main(args.model, args.features)