import pandas as pd

df = pd.read_parquet(
    "data/interim/player_match_stats.parquet"
)

print(df.head())
print(df.describe())