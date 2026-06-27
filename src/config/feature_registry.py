from pathlib import Path
from src.config.project_config import ROOT


FEATURE_SETS = {
    "top30": ROOT / "src/features/selection/top30_features.csv",
    "top40": ROOT / "src/features/selection/top40_features.csv",
    "top50": ROOT / "src/features/selection/top50_features.csv",
}


def load_feature_set(name: str):
    import pandas as pd

    path = FEATURE_SETS[name]

    return (
        pd.read_csv(path)["feature"]
        .tolist()
    )