import glob
import os
import pandas as pd

from src.config.project_config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    REPORTS_DIR,
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TEAM_SQUADS_DIR = (
    RAW_DATA_DIR
    / "team_squads"
)

PLAYERS_FILE = (
    RAW_DATA_DIR
    / "players"
    / "players.csv"
)

OUTPUT_DIR = (
    PROCESSED_DATA_DIR
    / "team_player_features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def obtener_ultimo_team_squads():

    archivos = glob.glob(
       str(
            TEAM_SQUADS_DIR / "team_squads_*.csv"
        )
    )

    if not archivos:
        raise FileNotFoundError(
            "No se encontraron archivos team_squads"
        )

    return max(
        archivos,
        key=os.path.getmtime
    )


def main():

    team_squads_file = obtener_ultimo_team_squads()

    print(
        f"\nLeyendo squads:\n{team_squads_file}"
    )

    squads = pd.read_csv(
        team_squads_file,
        low_memory=False
    )

    print(
        f"\nLeyendo players:\n{PLAYERS_FILE}"
    )

    players = pd.read_csv(
        PLAYERS_FILE,
        low_memory=False
    )

    # -------------------------------------------------
    # Preparar IDs
    # -------------------------------------------------

    squads["player_id"] = pd.to_numeric(
        squads["player_id"],
        errors="coerce"
    )

    players["player_id"] = pd.to_numeric(
        players["player_id"],
        errors="coerce"
    )

    squads = squads.dropna(
        subset=["player_id"]
    )

    players = players.dropna(
        subset=["player_id"]
    )

    squads["player_id"] = squads["player_id"].astype(int)
    players["player_id"] = players["player_id"].astype(int)

    # -------------------------------------------------
    # Merge
    # -------------------------------------------------

    df = squads.merge(
        players[
            [
                "player_id",
                "international_caps",
                "international_goals",
                "height_in_cm"
            ]
        ],
        on="player_id",
        how="left"
    )

    # -------------------------------------------------
    # Jugadores sin match por player_id
    # -------------------------------------------------

    missing = squads[
        ~squads["player_id"].isin(players["player_id"])
    ]

    missing.to_csv(
        REPORTS_DIR / "player_match_missing.csv",
        index=False
    )

    print(
        f"Jugadores sin información en players.csv: {len(missing)}"
    )

    print(
        f"Cobertura global: {(1 - len(missing)/len(squads))*100:.2f}%"
    )

    # Indicador de jugadores con información disponible
    df["has_stats"] = (
        df[
            [
                "height_in_cm",
                "international_caps",
                "international_goals"
            ]
        ]
        .notna()
        .any(axis=1)
    )
    # -------------------------------------------------
    # Match rate
    # -------------------------------------------------

    match_rate = (
        df["has_stats"]
        .mean()
        * 100
    )

    print(
        f"\nMatch rate: {match_rate:.2f}%"
    )

    # -------------------------------------------------
    # Features por equipo
    # -------------------------------------------------

    registros = []

    for team, g in df.groupby("team"):

        registros.append({

            "team": team,

            "avg_caps":
            g["international_caps"].mean(),

            "avg_int_goals":
            g["international_goals"].mean(),

            "avg_height":
            g["height_in_cm"].mean(),

            "players_with_stats":
            g["has_stats"].sum(),

            "players_total":
            len(g),

            "stats_coverage":
            g["has_stats"].mean()

        })

    df_out = pd.DataFrame(
        registros
    )

    # -------------------------------------------------
    # Guardar
    # -------------------------------------------------

    fecha = os.path.basename(team_squads_file)

    fecha = (
        fecha
        .replace("team_squads_", "")
        .replace(".csv", "")
    )

    output_file = (
        OUTPUT_DIR
        / f"team_player_features_{fecha}.csv"
    )

    df_out.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nArchivo generado:\n{output_file}"
    )

    print(
        f"Equipos: {len(df_out)}"
    )


if __name__ == "__main__":
    main()