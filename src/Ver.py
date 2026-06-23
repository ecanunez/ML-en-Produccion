import pandas as pd

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(ROOT / "src" / "models")
)

from load_dataset import load_dataset

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

# pd.set_option('display.max_columns', None)

# # Print your DataFrame
# print(df)

# print(df.shape)

# print(df["target"].value_counts(normalize=True))

import pandas as pd

analysis_df = pd.read_csv(
    "src/reports/error_analysis_predictions.csv"
)

draw_errors = analysis_df[
    analysis_df["real"] == "DRAW"
]

#print(draw_errors)

import pandas as pd

df = pd.read_csv(
    "src/reports/error_analysis_predictions.csv"
)

draws = df[df["real"] == "DRAW"]

draw_correct = draws[
    draws["pred"] == "DRAW"
]

draw_wrong = draws[
    draws["pred"] != "DRAW"
]

# print(len(draw_correct))
# print(len(draw_wrong))

cols = [
    "abs_elo_diff",
    "elo_diff",
    "abs_market_value_diff",
    "market_value_diff",
    "abs_points_diff",
    "points_diff",
    "balance_score",
    "caps_diff",
    "abs_caps_diff",
    "age_diff",
    "abs_age_diff"
]

comparison = pd.DataFrame({
    "DRAW_detectados":
        draw_correct[cols].mean(),

    "DRAW_perdidos":
        draw_wrong[cols].mean()
})

# print(comparison.round(2))

# print(
#       draw_correct["abs_elo_diff"].describe(),
#       draw_wrong["abs_elo_diff"].describe()
# )

# print(
#     draw_correct["abs_market_value_diff"].describe(),
#     draw_wrong["abs_market_value_diff"].describe()
# )

# print(
#     draw_correct["balance_score"].describe(),
#     draw_wrong["balance_score"].describe()
# )

# cols = [
#     "elo_diff",
#     "abs_elo_diff",
#     "market_value_diff",
#     "abs_market_value_diff",
#     "points_diff",
#     "abs_points_diff",
#     "caps_diff",
#     "abs_caps_diff",
#     "balance_score"
# ]

# draw_ok = draws[
#     draws["pred"] == "DRAW"
# ]

# draw_home = draws[
#     draws["pred"] == "HOME"
# ]

# draw_away = draws[
#     draws["pred"] == "AWAY"
# ]

# comparison = pd.DataFrame({
#     "DRAW_OK": draw_ok[cols].mean(),
#     "DRAW_TO_HOME": draw_home[cols].mean(),
#     "DRAW_TO_AWAY": draw_away[cols].mean()
# })

# print(comparison.round(2))

import pandas as pd

# df = pd.read_parquet(
#     "data/interim/elo_features.parquet"
# )

# print(df.columns)

# print(df[
#     [
#         "home_elo",
#         "away_elo",
#         "elo_diff"
#     ]
# ].head())

# print()

# print(df["elo_diff"].describe())

# df = pd.read_parquet(
#     "data/interim/new_elo_features.parquet"
# )

# print(df.describe())

# df = pd.read_parquet(
#     "data/processed/training_dataset.parquet"
# )

# print(
#     df[
#         [
#             "elo_home_win_prob",
#             "elo_away_win_prob",
#             "elo_draw_proxy",
#             "elo_favorite_strength"
#         ]
#     ].describe()
# )


from load_dataset import load_dataset
import pandas as pd

importance = pd.read_csv(
    "src/reports/feature_importance_rf_v2.csv"
)

X, y, features, _ = load_dataset()

importance_features = set(
    importance["feature"]
)

dataset_features = set(
    features
)

missing = sorted(
    importance_features - dataset_features
)

print(len(missing))
print(missing)