import pandas as pd

def build_last_tokens(name, n_tokens):

    tokens = str(name).strip().split()

    if len(tokens) < n_tokens:
        return None

    return " ".join(tokens[-n_tokens:])

players_df = pd.read_csv(
    "data/raw/players/players.csv"
)

players_df = players_df[
    players_df["last_season"] >= 2021
]

# print(players_df.shape)

# print(
#     players_df["last_season"]
#     .value_counts()
#     .sort_index()
# )

import pandas as pd

players = pd.read_csv(
    "data/raw/players/players.csv"
)

players = players[
    players["last_season"] >= 2021
]

for texto in [
    "Ben Yedder",
    "Ben Seghir",
    "Ben Slimane",
    "Bel Hassani",
    "Beka Beka",
    "Abu Fani"
]:

    # print("\n" + "=" * 50)
    # print(texto)

    resultado = players[
        players["name"]
        .str.contains(
            texto,
            case=False,
            na=False
        )
    ][["player_id", "name"]]

    print(resultado.head(20))

players["surname_1"] = (
    players["name"]
    .apply(lambda x: build_last_tokens(x, 1))
)

players["surname_2"] = (
    players["name"]
    .apply(lambda x: build_last_tokens(x, 2))
)

players["surname_3"] = (
    players["name"]
    .apply(lambda x: build_last_tokens(x, 3))
)

# print(
#     players[
#         players["name"]
#         .str.contains(
#             "Yedder|Hassani|Beka|Fani",
#             case=False,
#             na=False
#         )
#     ][[
#         "name",
#         "surname_1",
#         "surname_2",
#         "surname_3"
#     ]]
# )

players_df[
    players_df["name"]
    .str.contains("kja", case=False, na=False)
][["player_id", "name"]]

print(
    players_df[
        players_df["name"]
        .str.contains(
            "Slimane",
            case=False,
            na=False
        )
    ][
        ["player_id", "name", "last_season"]
    ]
)