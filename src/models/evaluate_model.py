from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix
)


# =========================================================
# STANDARD CLASSIFICATION EVALUATION
# =========================================================

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

    y_test : pd.Series

    model_name : str, optional

    verbose : bool, default=True

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

    cm = confusion_matrix(
        y_test,
        preds
    )

    report = classification_report(
        y_test,
        preds,
        digits=4,
        zero_division=0
    )

    if verbose:

        print("\n" + "=" * 60)

        if model_name:
            print(model_name)

        print("=" * 60)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1 Macro: {f1_macro:.4f}")
        print(f"Precision Macro: {precision_macro:.4f}")
        print(f"Recall Macro: {recall_macro:.4f}")

        print("\nConfusion Matrix")

        print(cm)

        print("\nClassification Report")

        print(report)

    return {
        "accuracy": accuracy,
        "f1_macro": f1_macro,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "confusion_matrix": cm.tolist(),
        "classification_report": report
    }


# =========================================================
# BOOSTING MODELS
# =========================================================

def evaluate_boosting_model(
    model,
    X_test,
    y_true,
    label_encoder,
    model_name=None,
    verbose=True
):

    preds_encoded = model.predict(X_test)

    preds = label_encoder.inverse_transform(
        preds_encoded.astype(int)
    )

    y_true = label_encoder.inverse_transform(
        y_true.astype(int)
    )

    accuracy = accuracy_score(
        y_true,
        preds
    )

    f1_macro = f1_score(
        y_true,
        preds,
        average="macro"
    )

    precision_macro = precision_score(
        y_true,
        preds,
        average="macro",
        zero_division=0
    )

    recall_macro = recall_score(
        y_true,
        preds,
        average="macro",
        zero_division=0
    )

    cm = confusion_matrix(
        y_true,
        preds
    )

    report = classification_report(
        y_true,
        preds,
        digits=4,
        zero_division=0
    )

    if verbose:

        print("\n" + "=" * 60)

        if model_name:
            print(model_name)

        print("=" * 60)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1 Macro: {f1_macro:.4f}")
        print(f"Precision Macro: {precision_macro:.4f}")
        print(f"Recall Macro: {recall_macro:.4f}")

        print("\nConfusion Matrix")

        print(cm)

        print("\nClassification Report")

        print(report)

    return {
        "accuracy": accuracy,
        "f1_macro": f1_macro,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "confusion_matrix": cm.tolist(),
        "classification_report": report
    }