import re
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"
PLAYERS_DIR = ROOT / "data" / "raw" / "players"

SQUADS_PATH = RAW_DIR / "fifa_worldcup_squads.parquet"
PLAYERS_PATH = PLAYERS_DIR / "players.csv"

OUTPUT_PATH = INTERIM_DIR / "worldcup_player_mapping.parquet"
REVIEW_PATH = INTERIM_DIR / "worldcup_player_mapping_review.csv"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)


def normalize_name(value):
    if pd.isna(value):
        return None

    value = str(value).lower().strip()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value if value else None


def build_worldcup_player_mapping():
    print("Leyendo planteles FIFA...")
    squads = pd.read_parquet(SQUADS_PATH)

    print("Leyendo players.csv...")
    players = pd.read_csv(PLAYERS_PATH)

    squads["player_name_norm"] = squads["player_name"].apply(normalize_name)
    players["player_name_norm"] = players["name"].apply(normalize_name)

    player_cols = [
        col for col in [
            "player_id",
            "name",
            "market_value_in_eur",
            "highest_market_value_in_eur",
            "date_of_birth",
            "height_in_cm",
            "country_of_citizenship",
            "country_of_birth",
            "position",
            "sub_position",
            "current_club_name",
        ]
        if col in players.columns
    ]

    players_small = players[player_cols + ["player_name_norm"]].copy()

    value_col = (
        "market_value_in_eur"
        if "market_value_in_eur" in players_small.columns
        else "highest_market_value_in_eur"
        if "highest_market_value_in_eur" in players_small.columns
        else None
    )

    if value_col:
        players_small = (
            players_small
            .sort_values(value_col, ascending=False, na_position="last")
            .drop_duplicates("player_name_norm", keep="first")
        )
    else:
        players_small = players_small.drop_duplicates("player_name_norm", keep="first")

    mapping = squads.merge(
        players_small,
        on="player_name_norm",
        how="left",
        suffixes=("_fifa", "_kaggle"),
    )

    mapping["matched"] = mapping["player_id"].notna()
    mapping["match_method"] = mapping["matched"].map(
        {True: "exact_normalized_name", False: "not_matched"}
    )

    mapping.to_parquet(OUTPUT_PATH, index=False)

    review_cols = [
        "team",
        "fifa_code",
        "confederation",
        "player_name",
        "position_fifa" if "position_fifa" in mapping.columns else "position",
        "player_name_norm",
        "matched",
        "match_method",
        "player_id",
        "name",
        "market_value_in_eur" if "market_value_in_eur" in mapping.columns else None,
        "country_of_citizenship" if "country_of_citizenship" in mapping.columns else None,
        "current_club_name" if "current_club_name" in mapping.columns else None,
    ]

    review_cols = [col for col in review_cols if col is not None and col in mapping.columns]

    mapping[review_cols].to_csv(
        REVIEW_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n============================================================")
    print("WORLD CUP PLAYER MAPPING FINALIZADO")
    print("============================================================")
    print(f"Jugadores FIFA: {len(mapping)}")
    print(f"Jugadores matcheados: {mapping['matched'].sum()}")
    print(f"Match rate: {mapping['matched'].mean():.2%}")
    print(f"Archivo parquet:")
    print(OUTPUT_PATH)
    print(f"Archivo revisión:")
    print(REVIEW_PATH)

    print("\nMatch rate por selección:")
    print(
        mapping
        .groupby("team")["matched"]
        .mean()
        .sort_values()
        .to_string()
    )

    return mapping


if __name__ == "__main__":
    build_worldcup_player_mapping()