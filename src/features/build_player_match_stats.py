from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

MATCHES_FILE = (
    ROOT / "data" / "interim" / "matches.parquet"
)

MAPPING_FILE = (
    ROOT / "data" / "interim" / "player_mapping.parquet"
)

PLAYERS_FILE = (
    ROOT / "data" / "raw" / "players" / "players.csv"
)

OUTPUT_FILE = (
    ROOT
    / "data"
    / "interim"
    / "player_match_stats.parquet"
)


def get_player_ids(match_row, side, player_lookup):

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


def compute_team_stats(
    player_ids,
    players_df
):

    squad = players_df[
        players_df["player_id"]
        .isin(player_ids)
    ]

    return {
        "players_found": len(squad),
        "team_market_value": squad[
            "market_value_in_eur"
        ].fillna(0).sum()
    }


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
    # Mapping válido
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
            "market_value_in_eur"
        ]
    ].copy()

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

            "match_idx": idx,

            "home_players_found":
                home_stats[
                    "players_found"
                ],

            "away_players_found":
                away_stats[
                    "players_found"
                ],

            "home_team_market_value":
                home_stats[
                    "team_market_value"
                ],

            "away_team_market_value":
                away_stats[
                    "team_market_value"
                ]
        }

        row[
            "market_value_diff"
        ] = (
            row[
                "home_team_market_value"
            ]
            -
            row[
                "away_team_market_value"
            ]
        )

        rows.append(row)

    output = pd.DataFrame(rows)

    print(
        f"\nFilas generadas: "
        f"{len(output):,}"
    )

    print(
        "\nValores faltantes:"
    )

    print(
        output.isna()
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
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

    