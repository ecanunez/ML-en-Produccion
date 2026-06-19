from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

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
        if c not in [
            "match_idx",
            "target",

            "home_elo",
            "away_elo",

            "home_team_market_value_mean",
            "away_team_market_value_mean",
            "home_team_market_value",
            "away_team_market_value",

            "home_GK_market_value_mean",
            "away_GK_market_value_mean",
            "home_GK_market_value_sum",
            "away_GK_market_value_sum",

            "home_DEF_market_value_mean",
            "away_DEF_market_value_mean",
            "home_DEF_market_value_sum",
            "away_DEF_market_value_sum",

            "home_MID_market_value_mean",
            "away_MID_market_value_mean",
            "home_MID_market_value_sum",
            "away_MID_market_value_sum",

            "home_ATT_market_value_mean",
            "away_ATT_market_value_mean",
            "home_ATT_market_value_sum",
            "away_ATT_market_value_sum"

        ]
    ]

    print(
        f"Features utilizadas: "
        f"{len(features)}"
    )

    X = df[features]

    y = df["target"]

    return X, y, features