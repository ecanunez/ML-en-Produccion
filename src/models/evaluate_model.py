from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix
)


def evaluate_model(
    model,
    X_test,
    y_test,
    model_name=None,
    verbose=True
):
    """
    Evalúa un modelo de clasificación multiclase.

    Parameters
    ----------
    model : estimator
        Modelo entrenado.

    X_test : pd.DataFrame
        Features de test.

    y_test : pd.Series
        Variable objetivo de test.

    model_name : str, optional
        Nombre del modelo para mostrar en pantalla.

    verbose : bool, default=True
        Si True imprime métricas detalladas.

    Returns
    -------
    dict
        Diccionario con métricas de evaluación.
    """

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

    precision_macro = precision_score(
        y_test,
        preds,
        average="macro",
        zero_division=0
    )

    recall_macro = recall_score(
        y_test,
        preds,
        average="macro",
        zero_division=0
    )

    if verbose:

        print("\n" + "=" * 60)

        if model_name:
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

        print(
            f"Precision Macro: "
            f"{precision_macro:.4f}"
        )

        print(
            f"Recall Macro: "
            f"{recall_macro:.4f}"
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

    return {
        "accuracy": accuracy,
        "f1_macro": f1_macro,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro
    }