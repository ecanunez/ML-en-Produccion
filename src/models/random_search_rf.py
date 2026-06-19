from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold
)

from load_dataset import load_dataset


def main():

    X, y, features = load_dataset()

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    param_dist = {

        "n_estimators": [
            300,
            500,
            800,
            1000
        ],

        "max_depth": [
            8,
            10,
            12,
            15,
            20,
            None
        ],

        "min_samples_split": [
            2,
            5,
            10
        ],

        "min_samples_leaf": [
            1,
            2,
            5,
            10
        ],

        "class_weight": [
            "balanced",
            "balanced_subsample"
        ]
    }

    rf = RandomForestClassifier(
        random_state=42,
        n_jobs=-1
    )

    search = RandomizedSearchCV(
        estimator=rf,
        param_distributions=param_dist,
        n_iter=30,
        scoring="f1_macro",
        cv=cv,
        verbose=2,
        random_state=42,
        n_jobs=-1,
        return_train_score=True
    )

    print("\nIniciando búsqueda...\n")

    search.fit(X, y)

    print("\n" + "=" * 60)
    print("MEJORES PARÁMETROS")
    print("=" * 60)

    print(search.best_params_)

    print("\nBest CV F1 Macro:")

    print(
        round(
            search.best_score_,
            4
        )
    )


if __name__ == "__main__":
    main()