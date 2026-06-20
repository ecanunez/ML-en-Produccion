from pathlib import Path
import pandas as pd

LOG_FILE = Path("src/reports/experiment_log.csv")


def log_experiment(
    dataset,
    model,
    f1_macro,
    accuracy,
    features,
    train_rows,
    notes="",
    params=""
):

    row = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "dataset": dataset,
        "model": model,
        "f1_macro": round(f1_macro, 4),
        "accuracy": round(accuracy, 4),
        "n_features": features,
        "train_rows": train_rows,
        "params": params,
        "notes": notes
    }])

    if LOG_FILE.exists():

        existing = pd.read_csv(LOG_FILE)

        row = pd.concat(
            [existing, row],
            ignore_index=True
        )

    row.to_csv(
        LOG_FILE,
        index=False
    )

    print("✓ Experimento registrado")