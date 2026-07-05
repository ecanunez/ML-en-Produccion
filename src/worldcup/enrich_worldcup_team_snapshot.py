from pathlib import Path

import pandas as pd


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"

MAPPING_PATH = INTERIM_DIR / "worldcup_player_mapping.parquet"
SNAPSHOT_PATH = INTERIM_DIR / "worldcup_team_snapshot.parquet"

OUTPUT_PATH = INTERIM_DIR / "worldcup_team_snapshot_enriched.parquet"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# CONFIG
# =========================================================

POSITION_MAP = {
    "Arquero": "GK",
    "Defensor": "DEF",
    "Mediocampista": "MID",
    "Delantero": "ATT",
}


# =========================================================
# HELPERS
# =========================================================

def safe_numeric(series):
    return pd.to_numeric(
        series,
        errors="coerce"
    )


def calculate_age(date_of_birth, reference_date="2026-06-01"):
    dob = pd.to_datetime(
        date_of_birth,
        errors="coerce"
    )

    ref = pd.Timestamp(reference_date)

    return (ref - dob).dt.days / 365.25


# =========================================================
# MAIN
# =========================================================

def enrich_worldcup_team_snapshot():
    print("Leyendo mapping FIFA -> players.csv...")
    mapping = pd.read_parquet(MAPPING_PATH)

    print("Leyendo snapshot base...")
    snapshot_base = pd.read_parquet(SNAPSHOT_PATH)

    # -----------------------------------------------------
    # Normalización columnas necesarias
    # -----------------------------------------------------

    if "position_group" not in mapping.columns:
        if "position_fifa" in mapping.columns:
            mapping["position_group"] = mapping["position_fifa"].map(POSITION_MAP)
        elif "position" in mapping.columns:
            mapping["position_group"] = mapping["position"].map(POSITION_MAP)
        else:
            raise ValueError(
                "No se encontró columna de posición FIFA. "
                "Columnas disponibles: "
                f"{mapping.columns.tolist()}"
            )

    if "market_value_in_eur" not in mapping.columns:
        mapping["market_value_in_eur"] = pd.NA

    if "height_in_cm" not in mapping.columns:
        mapping["height_in_cm"] = pd.NA

    if "date_of_birth" not in mapping.columns:
        mapping["date_of_birth"] = pd.NaT

    mapping["market_value_in_eur"] = safe_numeric(
        mapping["market_value_in_eur"]
    )

    mapping["height_in_cm"] = safe_numeric(
        mapping["height_in_cm"]
    )

    mapping["age"] = calculate_age(
        mapping["date_of_birth"]
    )

    # Placeholders porque todavía no vienen del mapping actual
    if "caps" not in mapping.columns:
        mapping["caps"] = pd.NA

    if "int_goals" not in mapping.columns:
        mapping["int_goals"] = pd.NA

    mapping["caps"] = safe_numeric(mapping["caps"])
    mapping["int_goals"] = safe_numeric(mapping["int_goals"])

    # -----------------------------------------------------
    # Agregados por selección
    # -----------------------------------------------------

    team_features = (
        mapping
        .groupby(
            ["team", "fifa_slug", "fifa_code", "confederation"],
            as_index=False
        )
        .agg(
            players_found=("player_name", "nunique"),
            players_matched=("matched", "sum"),
            team_market_value=("market_value_in_eur", "sum"),
            avg_player_value=("market_value_in_eur", "mean"),
            avg_age=("age", "mean"),
            avg_caps=("caps", "mean"),
            avg_height=("height_in_cm", "mean"),
            avg_int_goals=("int_goals", "mean"),
        )
    )

    # -----------------------------------------------------
    # Agregados por posición
    # -----------------------------------------------------

    position_values = (
        mapping
        .pivot_table(
            index=["team", "fifa_slug", "fifa_code", "confederation"],
            columns="position_group",
            values="market_value_in_eur",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    position_values.columns.name = None

    for col in ["GK", "DEF", "MID", "ATT"]:
        if col not in position_values.columns:
            position_values[col] = 0

    position_values = position_values.rename(
        columns={
            "GK": "GK_market_value_sum",
            "DEF": "DEF_market_value_sum",
            "MID": "MID_market_value_sum",
            "ATT": "ATT_market_value_sum",
        }
    )

    enriched = team_features.merge(
        position_values,
        on=["team", "fifa_slug", "fifa_code", "confederation"],
        how="left"
    )

    # -----------------------------------------------------
    # Conteos por posición desde snapshot base
    # -----------------------------------------------------

    count_cols = [
        "team",
        "GK_players",
        "DEF_players",
        "MID_players",
        "ATT_players",
    ]

    enriched = enriched.merge(
        snapshot_base[count_cols],
        on="team",
        how="left"
    )

    # -----------------------------------------------------
    # Orden final
    # -----------------------------------------------------

    ordered_columns = [
        "team",
        "fifa_slug",
        "fifa_code",
        "confederation",
        "players_found",
        "players_matched",
        "GK_players",
        "DEF_players",
        "MID_players",
        "ATT_players",
        "team_market_value",
        "avg_player_value",
        "avg_age",
        "avg_caps",
        "avg_height",
        "avg_int_goals",
        "GK_market_value_sum",
        "DEF_market_value_sum",
        "MID_market_value_sum",
        "ATT_market_value_sum",
    ]

    enriched = enriched[ordered_columns]

    enriched.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print("\n============================================================")
    print("WORLD CUP TEAM SNAPSHOT ENRICHED FINALIZADO")
    print("============================================================")
    print(f"Selecciones: {len(enriched)}")
    print(f"Archivo guardado en:")
    print(OUTPUT_PATH)

    print("\nResumen:")
    print(
        enriched[
            [
                "team",
                "players_found",
                "players_matched",
                "team_market_value",
                "avg_age",
                "avg_height",
            ]
        ].to_string(index=False)
    )

    return enriched


if __name__ == "__main__":
    enrich_worldcup_team_snapshot()