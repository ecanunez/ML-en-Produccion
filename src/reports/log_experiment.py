from pathlib import Path
import pandas as pd

LOG_FILE = Path("src/reports/experiment_log.csv")


def log_experiment(
    dataset,
    model,
    f1_macro,
    accuracy,
    features,
    notes=""
):

    row = pd.DataFrame([{
        "date": pd.Timestamp.now().date(),
        "dataset": dataset,
        "model": model,
        "f1_macro": f1_macro,
        "accuracy": accuracy,
        "features": features,
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

    print("Experimento registrado")