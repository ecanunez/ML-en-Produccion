import pandas as pd

df = pd.read_parquet(
    "data/processed/training_dataset.parquet"
)

df.groupby("target")[
    [
        "caps_diff",
        "age_diff",
        "int_goals_diff",
        "market_value_diff"
    ]
].mean()

print(df.groupby("target")[
    [
        "caps_diff",
        "age_diff",
        "int_goals_diff",
        "market_value_diff"
    ]
    ].mean()
)   

print(df.groupby("target")[
        [
            "abs_elo_diff",
            "abs_market_value_diff",
            "abs_caps_diff",
            "abs_age_diff"
        ]
    ].mean()
)

df["balance_score"] = (
    (df["abs_elo_diff"] < 80).astype(int)
    +
    (df["abs_market_value_diff"] < 50_000_000).astype(int)
    +
    (df["abs_caps_diff"] < 12).astype(int)
    +
    (df["abs_age_diff"] < 2).astype(int)
)

print(
    pd.crosstab(
        df["balance_score"],
        df["target"],
        normalize="index"
    )
)