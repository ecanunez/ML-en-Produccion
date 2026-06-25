import pandas as pd
import time

t0 = time.time()

players = pd.read_csv(
    "data/raw/players/players.csv",
    low_memory=False
)

# print(players.shape)
# print(time.time() - t0)

# print(
#     players[
#         players["player_id"].isin([
#             559319,
#             1371793,
#             258914
#         ])
#     ]
# )
missing = players[
    players["height_in_cm"].isna()
]

print(
    missing[
        [
            "player_id",
            "name",
            "current_club_name"
        ]
    ]
)

print(
    players.loc[
        players["player_id"] == 1371793,
        [
            "player_id",
            "name",
            "height_in_cm",
            "international_caps",
            "international_goals"
        ]
    ]
)

missing = pd.read_csv(
    "data/reports/player_match_missing.csv"
)

print(missing.head(20))

print(
    missing[
        [
            "team",
            "player_id",
            "player"
        ]
    ]
)