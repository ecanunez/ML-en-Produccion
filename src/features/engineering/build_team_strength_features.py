import pandas as pd

from src.config.project_config import (
    INTERIM_DATA_DIR
)

MATCHES_FILE = (
    INTERIM_DATA_DIR
    / "matches.parquet"
)

OUTPUT_FILE = (
    INTERIM_DATA_DIR
    / "team_strength_features.parquet"
)

WINDOW = 5

def get_team_history_features(
    history
):

    if len(history) == 0:

        return {
            "points_last5": 0,
            "win_rate_last5": 0,
            "gf_last5": 0,
            "ga_last5": 0,
            "gd_last5": 0
        }

    history = history.tail(WINDOW)

    points = history["points"].sum()

    wins = (
        history["points"] == 3
    ).sum()

    gf = history["gf"].sum()

    ga = history["ga"].sum()

    return {
        "points_last5": points,
        "win_rate_last5": wins / len(history),
        "gf_last5": gf,
        "ga_last5": ga,
        "gd_last5": gf - ga
    }


def main():

    print("Leyendo partidos...")

    matches = pd.read_parquet(
        MATCHES_FILE
    )

    matches = pd.read_parquet(
    MATCHES_FILE
)
    matches["fecha_partido"] = pd.to_datetime(
        matches["fecha_partido"]
    )

    matches = matches.sort_values(
        "fecha_partido"
    ).reset_index(
        drop=True
    )

    print(
        f"Partidos: {len(matches):,}"
    )

    team_history = {}

    rows = []

    print(
        "\nConstruyendo features..."
    )

    for idx, match in matches.iterrows():

        home_team = match["equipo_local"]

        away_team = match["equipo_visitante"]

        home_hist = (
            team_history.get(
                home_team,
                []
            )
        )

        away_hist = (
            team_history.get(
                away_team,
                []
            )
        )

        home_stats = (
            get_team_history_features(
                pd.DataFrame(home_hist)
            )
        )

        away_stats = (
            get_team_history_features(
                pd.DataFrame(away_hist)
            )
        )

        row = {
            "match_idx": idx
        }

        for k, v in home_stats.items():
            row[f"home_{k}"] = v

        for k, v in away_stats.items():
            row[f"away_{k}"] = v

        row["points_diff"] = (
            row["home_points_last5"]
            -
            row["away_points_last5"]
        )

        row["win_rate_diff"] = (
            row["home_win_rate_last5"]
            -
            row["away_win_rate_last5"]
        )

        row["gd_diff"] = (
            row["home_gd_last5"]
            -
            row["away_gd_last5"]
        )

        rows.append(row)

        # -------------------------
        # actualizar historial
        # -------------------------

        home_goals = match["goles_local"]

        away_goals = match["goles_visitante"]

        if home_goals > away_goals:

            home_points = 3
            away_points = 0

        elif home_goals < away_goals:

            home_points = 0
            away_points = 3

        else:

            home_points = 1
            away_points = 1

        team_history.setdefault(
            home_team,
            []
        ).append({
            "points": home_points,
            "gf": home_goals,
            "ga": away_goals
        })

        team_history.setdefault(
            away_team,
            []
        ).append({
            "points": away_points,
            "gf": away_goals,
            "ga": home_goals
        })

    output = pd.DataFrame(rows)

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

    print(
        "\nShape:"
    )

    print(output.shape)


if __name__ == "__main__":
    main()