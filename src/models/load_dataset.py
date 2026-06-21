from pathlib import Path
import pandas as pd
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(ROOT / "src")
)

from config.feature_config import EXCLUDED_COLUMNS

DATA_FILE = (
    ROOT
    / "data"
    / "processed"
    / "training_dataset.parquet"
)

def load_dataset():

    print("Leyendo dataset...")

    df = pd.read_parquet(DATA_FILE)

    print(
        f"Observaciones originales: "
        f"{len(df):,}"
    )

    df = df[
        df["target"].notna()
    ].copy()

    print(
        f"Observaciones finales: "
        f"{len(df):,}"
    )

    features = [
        c
        for c in df.columns
        if c not in EXCLUDED_COLUMNS
    ]

    print(
        f"Features utilizadas: "
        f"{len(features)}"
    )

    X = df[features]

    y = df["target"]

    dataset_modified = datetime.fromtimestamp(
        DATA_FILE.stat().st_mtime
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return (
        X,
        y,
        features,
        dataset_modified
    )