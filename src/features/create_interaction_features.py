import pandas as pd
import numpy as np

INPUT_FILE = "data/processed/training_dataset.parquet"

OUTPUT_FILE = (
    "data/interim/interaction_features.parquet"
)

def main():

    print("=" * 60)
    print("INTERACTION FEATURES")
    print("=" * 60)

    df = pd.read_parquet(INPUT_FILE)

    features = pd.DataFrame()

    features["match_idx"] = df["match_idx"]

    features["elo_market_interaction"] = (
        df["elo_diff"]
        *
        df["market_value_diff"]
    )

    features["elo_caps_interaction"] = (
        df["elo_diff"]
        *
        df["caps_diff"]
    )

    features["caps_goals_interaction"] = (
        df["caps_diff"]
        *
        df["int_goals_diff"]
    )

    features["attack_strength_interaction"] = (
        df["ATT_value_diff"]
        *
        df["int_goals_diff"]
    )

    features["value_per_elo"] = (
        df["market_value_diff"]
        /
        (np.abs(df["elo_diff"]) + 1)
    )

    features["caps_per_elo"] = (
        df["caps_diff"]
        /
        (np.abs(df["elo_diff"]) + 1)
    )

    print(features.head())

    features.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nArchivo generado:")
    print(OUTPUT_FILE)

if __name__ == "__main__":
    main()