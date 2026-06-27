import pandas as pd

from src.config.project_config import (
    INTERIM_DATA_DIR,
    RAW_DATA_DIR
)

MATCHES_FILE = (
    INTERIM_DATA_DIR
    / "matches.parquet"
)

MAPPING_FILE = (
    INTERIM_DATA_DIR
    / "player_mapping.parquet"
)

PLAYERS_FILE = (
    RAW_DATA_DIR
    / "players"
    / "players.csv"
)

OUTPUT_FILE = (
    INTERIM_DATA_DIR
    / "player_match_stats.parquet"
)

def get_player_ids(
    match_row,
    side,
    player_lookup
):

    ids = []

    for i in range(1, 12):

        player_name = match_row.get(
            f"{side}_jugador_{i}"
        )

        if player_name in player_lookup:

            ids.append(
                player_lookup[player_name]
            )

    return ids


def map_position(position):

    position = str(position).lower()

    if "goalkeeper" in position:
        return "GK"

    if position == "defender":
        return "DEF"

    if position == "midfield":
        return "MID"

    if position == "attack":
        return "ATT"

    return "UNK"


def compute_team_stats(
    player_ids,
    players_df
):

    squad = players_df[
        players_df["player_id"]
        .isin(player_ids)
    ].copy()

    result = {}

    result["players_found"] = len(
        squad
    )

    result["team_market_value"] = (
        squad["market_value_in_eur"]
        .fillna(0)
        .sum()
    )

    result["team_market_value_mean"] = (
        squad["market_value_in_eur"]
        .fillna(0)
        .mean()
    )

    for group in [
        "GK",
        "DEF",
        "MID",
        "ATT"
    ]:

        subset = squad[
            squad["position_group"]
            == group
        ]

        result[
            f"{group}_market_value_sum"
        ] = (
            subset["market_value_in_eur"]
            .fillna(0)
            .sum()
        )

        result[
            f"{group}_market_value_mean"
        ] = (
            subset["market_value_in_eur"]
            .fillna(0)
            .mean()
        )

        result[
            f"{group}_players"
        ] = len(subset)

    return result


def main():

    print("Leyendo archivos...")

    matches = pd.read_parquet(
        MATCHES_FILE
    )

    mapping = pd.read_parquet(
        MAPPING_FILE
    )

    players = pd.read_csv(
        PLAYERS_FILE
    )

    print(
        f"Partidos: {len(matches):,}"
    )

    # -------------------------
    # Mapping
    # -------------------------

    mapping = mapping[
        mapping["player_id"].notna()
    ].copy()

    mapping["player_id"] = (
        mapping["player_id"]
        .astype(int)
    )

    player_lookup = (
        mapping
        .set_index("lineup_name")
        ["player_id"]
        .to_dict()
    )

    print(
        f"Jugadores mapeados: "
        f"{len(player_lookup):,}"
    )

    # -------------------------
    # Players
    # -------------------------

    players = players[
        [
            "player_id",
            "position",
            "market_value_in_eur"
        ]
    ].copy()

    players["position_group"] = (
        players["position"]
        .apply(map_position)
    )

    rows = []

    print(
        "\nConstruyendo features..."
    )

    for idx, match in matches.iterrows():

        home_ids = get_player_ids(
            match,
            "local",
            player_lookup
        )

        away_ids = get_player_ids(
            match,
            "visitante",
            player_lookup
        )

        home_stats = compute_team_stats(
            home_ids,
            players
        )

        away_stats = compute_team_stats(
            away_ids,
            players
        )

        row = {
            "match_idx": idx
        }

        for k, v in home_stats.items():

            row[f"home_{k}"] = v

        for k, v in away_stats.items():

            row[f"away_{k}"] = v

        row["market_value_diff"] = (
            row["home_team_market_value"]
            -
            row["away_team_market_value"]
        )

        row["GK_value_diff"] = (
            row["home_GK_market_value_sum"]
            -
            row["away_GK_market_value_sum"]
        )

        row["DEF_value_diff"] = (
            row["home_DEF_market_value_sum"]
            -
            row["away_DEF_market_value_sum"]
        )

        row["MID_value_diff"] = (
            row["home_MID_market_value_sum"]
            -
            row["away_MID_market_value_sum"]
        )

        row["ATT_value_diff"] = (
            row["home_ATT_market_value_sum"]
            -
            row["away_ATT_market_value_sum"]
        )

        rows.append(row)

    output = pd.DataFrame(
        rows
    )

    print(
        f"\nFilas generadas: "
        f"{len(output):,}"
    )

    print(
        "\nColumnas generadas:"
    )

    print(
        output.columns.tolist()
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nArchivo generado:"
    )

    print(
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()