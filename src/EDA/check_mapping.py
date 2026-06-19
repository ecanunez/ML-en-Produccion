import pandas as pd

players = pd.read_csv(
    "data/raw/players/players.csv"
)

for nombre in [
    "Ben Slimane",
    "Kjaer",
    "Ulmer",
    "Meffert",
    "Zoubir"
]:

    print("\n" + "=" * 50)
    print(nombre)

    print(
        players[
            players["name"]
            .str.contains(
                nombre,
                case=False,
                na=False
            )
        ][[
            "player_id",
            "name",
            "last_season"
        ]]
    )