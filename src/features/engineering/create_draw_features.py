import pandas as pd


INPUT_FILE = (
    "data/interim/player_balance_features.parquet"
)

OUTPUT_FILE = (
    "data/interim/draw_features.parquet"
)


def main():

    print("=" * 60)
    print("DRAW FEATURES")
    print("=" * 60)

    df = pd.read_parquet(INPUT_FILE)

    features = pd.DataFrame()

    features["match_idx"] = df["match_idx"]

    # --------------------------------------------------
    # Zonas de equilibrio
    # --------------------------------------------------

    features["elo_draw_zone"] = (
        df["abs_elo_diff"] < 60
    ).astype(int)

    features["market_draw_zone"] = (
        df["abs_market_value_diff"] < 20_000_000
    ).astype(int)

    features["experience_draw_zone"] = (
        df["abs_caps_diff"] < 12
    ).astype(int)

    # --------------------------------------------------
    # Ultra balanceado
    # --------------------------------------------------

    features["ultra_balanced_match"] = (
        (
            df["abs_elo_diff"] < 40
        )
        &
        (
            df["abs_market_value_diff"] < 10_000_000
        )
    ).astype(int)

    # --------------------------------------------------
    # Score de empate
    # --------------------------------------------------

    features["draw_candidate_score"] = (
        (df["abs_elo_diff"] < 50).astype(int)
        +
        (df["abs_market_value_diff"] < 15_000_000).astype(int)
        +
        (df["abs_caps_diff"] < 10).astype(int)
        +
        (df["abs_points_diff"] < 3).astype(int)
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