from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

SQUADS_PATH = RAW_DIR / "fifa_worldcup_squads.parquet"
OUTPUT_PATH = INTERIM_DIR / "worldcup_team_snapshot.parquet"


POSITION_MAP = {
    "Arquero": "GK",
    "Defensor": "DEF",
    "Mediocampista": "MID",
    "Delantero": "ATT",
}


def build_worldcup_team_snapshot():
    print("Leyendo planteles FIFA...")
    squads = pd.read_parquet(SQUADS_PATH)

    squads["position_group"] = squads["position"].map(POSITION_MAP)

    # Conteo total de jugadores
    base = (
        squads
        .groupby(
            ["team", "fifa_slug", "fifa_code", "confederation"],
            as_index=False
        )
        .agg(
            players_found=("player_name", "nunique")
        )
    )

    # Conteo por posición
    position_counts = (
        squads
        .pivot_table(
            index=["team", "fifa_slug", "fifa_code", "confederation"],
            columns="position_group",
            values="player_name",
            aggfunc="nunique",
            fill_value=0
        )
        .reset_index()
    )

    position_counts.columns.name = None

    for col in ["GK", "DEF", "MID", "ATT"]:
        if col not in position_counts.columns:
            position_counts[col] = 0

    position_counts = position_counts.rename(
        columns={
            "GK": "GK_players",
            "DEF": "DEF_players",
            "MID": "MID_players",
            "ATT": "ATT_players",
        }
    )

    snapshot = base.merge(
        position_counts,
        on=["team", "fifa_slug", "fifa_code", "confederation"],
        how="left"
    )

    # Columnas esperadas para etapas posteriores.
    # Por ahora quedan NaN porque FIFA no aporta estos valores directamente.
    placeholder_columns = [
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

    for col in placeholder_columns:
        snapshot[col] = pd.NA

    ordered_columns = [
        "team",
        "fifa_slug",
        "fifa_code",
        "confederation",
        "players_found",
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

    snapshot = snapshot[ordered_columns]

    snapshot.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print("\n============================================================")
    print("WORLD CUP TEAM SNAPSHOT FINALIZADO")
    print("============================================================")
    print(f"Selecciones: {len(snapshot)}")
    print(f"Archivo guardado en:")
    print(OUTPUT_PATH)

    print("\nResumen jugadores por selección:")
    print(snapshot[["team", "players_found", "GK_players", "DEF_players", "MID_players", "ATT_players"]].to_string(index=False))

    return snapshot


if __name__ == "__main__":
    build_worldcup_team_snapshot()