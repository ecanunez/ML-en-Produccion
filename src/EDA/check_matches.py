# src/EDA/check_matches.py

import pandas as pd

df = pd.read_parquet("data/interim/matches_raw.parquet")

print("\nShape:")
print(df.shape)

print("\nColumnas:")
for c in df.columns:
    print(c)

print("\nPrimer registro:")
print(df.iloc[0])

print("\nPrimeras filas:")
print(df.head(3))