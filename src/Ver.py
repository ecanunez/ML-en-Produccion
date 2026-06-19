from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

MATCHES_FILE = (
    ROOT / "data" / "interim" / "matches.parquet"
)

MAPPING_FILE = (
    ROOT / "data" / "interim" / "player_mapping.parquet"
)

APPEARANCES_FILE = (
    ROOT / "data" / "raw" / "players" / "appearances.csv"
)

PLAYERS_FILE = (
    ROOT / "data" / "raw" / "players" / "players.csv"
)


def main():

    print("Leyendo archivos...")

    matches = pd.read_parquet(
        MATCHES_FILE
    )

    mapping = pd.read_parquet(
        MAPPING_FILE
    )

    appearances = pd.read_csv(
        APPEARANCES_FILE,
        usecols=[
            "player_name",
            "player_id"
        ]
    )

    players = pd.read_csv(
        PLAYERS_FILE,
        usecols=[
            "player_id"
        ]
    )

    # -------------------------
    # nombres de alineaciones
    # -------------------------

    lineup_columns = []

    for side in [
        "local",
        "visitante"
    ]:

        for i in range(1, 12):

            lineup_columns.append(
                f"{side}_jugador_{i}"
            )

    lineup_names = set()

    for col in lineup_columns:

        lineup_names.update(
            matches[col]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

    print(
        f"\nJugadores únicos en alineaciones: "
        f"{len(lineup_names):,}"
    )

    # -------------------------
    # player_mapping
    # -------------------------

    mapping_names = set(
        mapping["lineup_name"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    matched_mapping = (
        lineup_names
        &
        mapping_names
    )

    print(
        "\nEncontrados en player_mapping:"
    )

    print(
        f"{len(matched_mapping):,}"
    )

    print(
        f"Cobertura: "
        f"{100 * len(matched_mapping) / len(lineup_names):.2f}%"
    )

    # -------------------------
    # appearances
    # -------------------------

    appearance_names = set(
        appearances["player_name"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    matched_appearances = (
        lineup_names
        &
        appearance_names
    )

    print(
        "\nEncontrados en appearances:"
    )

    print(
        f"{len(matched_appearances):,}"
    )

    print(
        f"Cobertura: "
        f"{100 * len(matched_appearances) / len(lineup_names):.2f}%"
    )

    # -------------------------
    # faltantes
    # -------------------------

    missing_in_mapping = (
        lineup_names
        -
        mapping_names
    )

    missing_in_appearances = (
        lineup_names
        -
        appearance_names
    )

    print(
        "\nEjemplos faltantes en mapping:"
    )

    print(
        list(missing_in_mapping)[:20]
    )

    print(
        "\nEjemplos faltantes en appearances:"
    )

    print(
        list(missing_in_appearances)[:20]
    )

    # -------------------------
    # Auditoría IDs
    # -------------------------

    mapping_ids = set(
        mapping["player_id"]
        .dropna()
        .astype(int)
    )

    players_ids = set(
        players["player_id"]
        .dropna()
        .astype(int)
    )

    shared_ids = (
        mapping_ids
        &
        players_ids
    )

    print(
        "\n=============================="
    )

    print(
        "AUDITORÍA DE IDs"
    )

    print(
        "=============================="
    )

    print(
        f"IDs en mapping: "
        f"{len(mapping_ids):,}"
    )

    print(
        f"IDs en players: "
        f"{len(players_ids):,}"
    )

    print(
        f"IDs compartidos: "
        f"{len(shared_ids):,}"
    )

    print(
        f"Cobertura players.csv: "
        f"{100 * len(shared_ids) / len(mapping_ids):.2f}%"
    )

    missing_ids = list(
        mapping_ids
        -
        players_ids
    )

    print(
        "\nEjemplos de IDs presentes en mapping "
        "pero ausentes en players.csv:"
    )

    print(
        missing_ids[:20]
    )

    print(
        "\nMapping:"
    )

    print(
        mapping.shape
    )

    print(
        "\nlineup_name únicos:"
    )

    print(
        mapping["lineup_name"].nunique()
    )

    print(
        "\nplayer_id únicos:"
    )

    print(
        mapping["player_id"].nunique()
    )

    dup_ids = (
        mapping
        .groupby("player_id")
        .size()
        .sort_values(
            ascending=False
        )
    )

    print(
        "\nTop player_id repetidos:"
    )

    print(
        dup_ids.head(20)
    )

    dup_ids = (
        mapping
        .groupby("player_id")
        .size()
        .sort_values(ascending=False)
    )

    print("\nTop 20 player_id más repetidos:\n")

    print(
        dup_ids.head(20)
    )
    top_ids = dup_ids.head(10).index

    # for pid in top_ids:

    #     print("\n====================")
    #     print("PLAYER ID:", pid)

    #     print(
    #         mapping[
    #             mapping["player_id"] == pid
    #         ][
    #             "lineup_name"
    #         ].tolist()
    #     )
    print(
        "\n=============================="
    )

    print(
        "MÉTODOS DE MATCHING"
    )

    print(
        "=============================="
    )

    print(
        mapping["method"]
        .value_counts()
    )

    print()

    print(
        (
            mapping["method"]
            .value_counts(normalize=True)
            * 100
        ).round(2)
    )

if __name__ == "__main__":
    main()