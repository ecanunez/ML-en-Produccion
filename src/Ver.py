import pandas as pd

df = pd.read_parquet(
    "data/processed/training_dataset.parquet"
)

print(
    df.groupby("target")["elo_diff"]
      .agg(["count", "mean", "median"])
)