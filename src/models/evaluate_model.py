from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
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
            digits=4,
            zero_division=0
        )
    )