from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from load_dataset import load_dataset
from evaluate_model import evaluate_model
from log_experiment import log_experiment
from src.config.project_config import (
    RANDOM_STATE
)

def main():

    X, y, features, dataset_modified = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    hgb = HistGradientBoostingClassifier(
        learning_rate=0.05,
        max_depth=6,
        max_iter=300,
        min_samples_leaf=20,
        random_state=RANDOM_STATE
    )

    hgb.fit(
        X_train,
        y_train
    )

    metrics = evaluate_model(
        hgb,
        X_test,
        y_test,
        "HIST GRADIENT BOOSTING"
    )

    log_experiment(
        dataset="training_dataset.parquet",
        dataset_modified=dataset_modified,
        model="HistGradientBoosting",
        f1_macro=metrics["f1_macro"],
        accuracy=metrics["accuracy"],
        precision_macro=metrics["precision_macro"],
        recall_macro=metrics["recall_macro"],
        features=X.shape[1],
        train_rows=len(X_train),
        params=(
            "learning_rate=0.05,"
            "max_depth=6,"
            "max_iter=300,"
            "min_samples_leaf=20"
        ),
        notes="Feature Engineering v1"
    )


if __name__ == "__main__":
    main()