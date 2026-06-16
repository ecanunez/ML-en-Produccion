import pandas as pd

matches = pd.read_parquet(
    "data/interim/matches.parquet"
)

players_df = pd.read_csv(
    "data/raw/players/players.csv"
)

players_df = players_df[
    players_df["last_season"] >= 2021
]

player_cols = [
    c
    for c in matches.columns
    if "jugador" in c
]

match_players = pd.unique(
    matches[player_cols]
    .values.ravel()
)

match_players = {
    str(x).strip()
    for x in match_players
    if pd.notna(x)
}

tm_players = {
    str(x).strip()
    for x in players_df["name"].dropna()
}

exact_matches = (
    match_players &
    tm_players
)

#print("Jugadores alineaciones:", len(match_players))
#print("Coincidencias exactas:", len(exact_matches))

print(
    "Cobertura:",
    round(
        len(exact_matches)
        / len(match_players)
        * 100,
        2
    ),
    "%"
)

players_df["apellido"] = (
    players_df["name"]
    .str.split()
    .str[-1]
)

apellidos_tm = {
    str(x).strip()
    for x in players_df["apellido"].dropna()
}

apellido_matches = (
    match_players &
    apellidos_tm
)

print(
    "Coincidencias por apellido:",
    len(apellido_matches)
)

print(
    "Cobertura por apellido:",
    round(
        len(apellido_matches)
        / len(match_players)
        * 100,
        2
    ),
    "%"
)

players_df["apellido"] = (
    players_df["name"]
    .str.split()
    .str[-1]
)

conteo = (
    players_df
    .groupby("apellido")
    .size()
    .reset_index(name="cantidad")
)

print(
    conteo["cantidad"]
    .value_counts()
    .sort_index()
)

surname_counts = (
    players_df["apellido"]
    .value_counts()
)

unique_surnames = set(
    surname_counts[
        surname_counts == 1
    ].index
)

matchable_by_surname = [
    p
    for p in match_players
    if p in unique_surnames
]

print(
    "Match apellido único:",
    len(matchable_by_surname)
)

players_df[
    players_df["name"]
    .str.contains(
        "Slimane",
        case=False,
        na=False
    )
][["player_id","name"]]