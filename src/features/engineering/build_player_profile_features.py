import pandas as pd

from src.config.dataset_config import (
    INTERIM_DATA_DIR,
    RAW_DATA_DIR,
)

MATCHES_FILE = (
    INTERIM_DATA_DIR
    / "matches.parquet"
)

PLAYER_MAPPING_FILE = (
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
    / "player_profile_features.parquet"
)

def build_long(matches, side):

    rows = []

    prefix = (
        "local_jugador_"
        if side == "home"
        else "visitante_jugador_"
    )

    for i in range(1, 12):

        col = f"{prefix}{i}"

        tmp = matches[
            [
                "match_idx",
                "fecha_partido",
                col
            ]
        ].copy()

        tmp.columns = [
            "match_idx",
            "fecha_partido",
            "lineup_name"
        ]

        tmp["side"] = side

        rows.append(tmp)

    return pd.concat(
        rows,
        ignore_index=True
    )


def aggregate_side(df, prefix):

    agg = (
        df.groupby("match_idx")
        .agg({
            "age": "mean",
            "height_in_cm": "mean",
            "market_value_in_eur": "mean",
            "international_caps": "mean",
            "international_goals": "mean",
            "player_id": "count"
        })
        .reset_index()
    )

    agg = agg.rename(
        columns={
            "age": f"{prefix}_avg_age",
            "height_in_cm": f"{prefix}_avg_height",
            "market_value_in_eur": f"{prefix}_avg_player_value",
            "international_caps": f"{prefix}_avg_caps",
            "international_goals": f"{prefix}_avg_int_goals",
            "player_id": f"{prefix}_profile_players_found"
        }
    )

    return agg


def main():

    print("Leyendo datasets...")

    matches = pd.read_parquet(
        MATCHES_FILE
    )

    matches = matches.reset_index(
        drop=True
    )

    matches["match_idx"] = matches.index

    mapping = pd.read_parquet(
        PLAYER_MAPPING_FILE
    )

    players = pd.read_csv(
        PLAYERS_FILE,
        low_memory=False
    )

    print(f"Matches: {len(matches):,}")
    print(f"Mappings: {len(mapping):,}")
    print(f"Players: {len(players):,}")

    players = players[
        [
            "player_id",
            "date_of_birth",
            "height_in_cm",
            "market_value_in_eur",
            "international_caps",
            "international_goals"
        ]
    ].copy()

    players["date_of_birth"] = pd.to_datetime(
        players["date_of_birth"],
        errors="coerce"
    )

    home = build_long(
        matches,
        "home"
    )

    away = build_long(
        matches,
        "away"
    )

    long_df = pd.concat(
        [home, away],
        ignore_index=True
    )

    print(
        f"Alineaciones: {len(long_df):,}"
    )

    long_df = long_df.merge(
        mapping[
            [
                "lineup_name",
                "player_id"
            ]
        ],
        on="lineup_name",
        how="left"
    )

    long_df = long_df.merge(
        players,
        on="player_id",
        how="left"
    )

    long_df["age"] = (
        (
            pd.to_datetime(
                long_df["fecha_partido"]
            )
            - long_df["date_of_birth"]
        ).dt.days
        / 365.25
    )

    home_df = long_df[
        long_df["side"] == "home"
    ]

    away_df = long_df[
        long_df["side"] == "away"
    ]

    home_features = aggregate_side(
        home_df,
        "home"
    )

    away_features = aggregate_side(
        away_df,
        "away"
    )

    features = (
        home_features
        .merge(
            away_features,
            on="match_idx",
            how="outer"
        )
    )

    features["age_diff"] = (
        features["home_avg_age"]
        - features["away_avg_age"]
    )

    features["height_diff"] = (
        features["home_avg_height"]
        - features["away_avg_height"]
    )

    # features["player_value_diff"] = (
    #     features["home_avg_player_value"]
    #     - features["away_avg_player_value"]
    # )

    features["caps_diff"] = (
        features["home_avg_caps"]
        - features["away_avg_caps"]
    )

    features["int_goals_diff"] = (
        features["home_avg_int_goals"]
        - features["away_avg_int_goals"]
    )

    # features["profile_players_found_diff"] = (
    #     features["home_profile_players_found"]
    #     - features["away_profile_players_found"]
    # )

    features = features.fillna(0)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    features.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nArchivo generado:")
    print(OUTPUT_FILE)

    print(
        f"\nShape: {features.shape}"
    )

    print("\nCobertura promedio:")

    print(
        features[
            [
                "home_profile_players_found",
                "away_profile_players_found"
            ]
        ].mean()
    )


if __name__ == "__main__":
    main()