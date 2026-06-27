from pathlib import Path
import pandas as pd
from src.config.project_config import ROOT

FEATURE_SETS = {
    "top10": ROOT / "src/reports/top10_features.csv",
    "top20": ROOT / "src/reports/top20_features.csv",
    "top30": ROOT / "src/reports/top30_features.csv",
    "top40": ROOT / "src/reports/top40_features.csv",
    "top50": ROOT / "src/reports/top50_features.csv",
    "all": None
}


def load_feature_set(name: str):

    if name not in FEATURE_SETS:
        raise ValueError(f"Feature set desconocido: {name}")

    path = FEATURE_SETS[name]

    if path is None:
        return None

    df = pd.read_csv(path)

    return df["feature"].tolist()