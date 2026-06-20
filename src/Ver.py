import pandas as pd

df = pd.read_parquet(
    "data/processed/training_dataset.parquet"
)

# cols = [
#     c
#     for c in df.columns
#     if "profile" in c
#     or "avg_age" in c
#     or "avg_caps" in c
#     or "player_value_diff" in c
# ]

# print(cols)

# print(
#     df[cols]
#     .describe()
# )

# print(df[cols].corr())

# cols = [
#     "age_diff",
#     "caps_diff",
#     "market_value_diff",
#     "elo_diff",
# ]

# print(df[cols].corr())

pd.set_option('display.max_columns', None)

# Print your DataFrame
print(df)