import pandas as pd

INPUT_PATH = (
    "data/interim/elo_features.parquet"
)

OUTPUT_PATH = (
    "data/interim/new_elo_features.parquet"
)

print("=" * 60)
print("NEW ELO FEATURES")
print("=" * 60)

df = pd.read_parquet(INPUT_PATH)

df_new = pd.DataFrame()

df_new["match_idx"] = df["match_idx"]

df_new["elo_home_win_prob"] = (
    1 /
    (
        1 +
        10 ** (
            -df["elo_diff"] / 400
        )
    )
)

df_new["elo_away_win_prob"] = (
    1 -
    df_new["elo_home_win_prob"]
)

df_new["elo_draw_proxy"] = (
    1 -
    (
        abs(
            df_new["elo_home_win_prob"]
            - 0.5
        ) * 2
    )
)

df_new["elo_favorite_strength"] = (
    abs(
        df_new["elo_home_win_prob"]
        - 0.5
    )
)

print(df_new.head())

df_new.to_parquet(
    OUTPUT_PATH,
    index=False
)

print()
print("Archivo generado:")
print(OUTPUT_PATH)