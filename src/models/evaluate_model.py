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

    accuracy = accuracy_score(
        y_test,
        preds
    )

    f1_macro = f1_score(
        y_test,
        preds,
        average="macro"
    )

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    print(
        f"Accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"F1 Macro: "
        f"{f1_macro:.4f}"
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

    return (
        accuracy_score(y_test, preds),
        f1_score(y_test, preds, average="macro")
    )