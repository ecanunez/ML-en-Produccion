from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from load_dataset import load_dataset
from evaluate_model import evaluate_model
from log_experiment import log_experiment


def main():

    X, y, features, dataset_modified = load_dataset()

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

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

    metrics = evaluate_model(
        rf,
        X_test,
        y_test,
        "RANDOM FOREST"
    )

    log_experiment(
        dataset="training_dataset.parquet",
        dataset_modified=dataset_modified,
        model="Random Forest",
        f1_macro=metrics["f1_macro"],
        accuracy=metrics["accuracy"],
        precision_macro=metrics["precision_macro"],
        recall_macro=metrics["recall_macro"],
        features=X.shape[1],
        train_rows=len(X_train)
        params=(
            "n_estimators=500,"
            "max_depth=12,"
            "min_samples_leaf=5,"
            "min_samples_split=2,"
            "class_weight=balanced"
        ),
        notes="Feature Engineering v1"
    )


if __name__ == "__main__":
    main()