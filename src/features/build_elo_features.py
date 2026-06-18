from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

MATCHES_FILE = (
    ROOT
    / "data"
    / "interim"
    / "matches.parquet"
)

OUTPUT_FILE = (
    ROOT
    / "data"
    / "interim"
    / "elo_features.parquet"
)

INITIAL_ELO = 1500
K_FACTOR = 20


def expected_score(
    rating_a,
    rating_b
):

    return (
        1
        /
        (
            1
            + 10 ** (
                (rating_b - rating_a)
                / 400
            )
        )
    )


def update_elo(
    rating_home,
    rating_away,
    result
):

    expected_home = expected_score(
        rating_home,
        rating_away
    )

    expected_away = expected_score(
        rating_away,
        rating_home
    )

    if result == "HOME":

        score_home = 1.0
        score_away = 0.0

    elif result == "AWAY":

        score_home = 0.0
        score_away = 1.0

    else:

        score_home = 0.5
        score_away = 0.5

    new_home = (
        rating_home
        +
        K_FACTOR
        * (
            score_home
            - expected_home
        )
    )

    new_away = (
        rating_away
        +
        K_FACTOR
        * (
            score_away
            - expected_away
        )
    )

    return (
        new_home,
        new_away
    )


def get_match_result(row):

    home_goals = row["goles_local"]
    away_goals = row["goles_visitante"]

    if home_goals > away_goals:
        return "HOME"

    if away_goals > home_goals:
        return "AWAY"

    return "DRAW"


def main():

    print("Leyendo partidos...")

    matches = pd.read_parquet(
        MATCHES_FILE
    )

    matches = matches.sort_values(
        "fecha_partido"
    ).reset_index()

    print(
        f"Partidos: {len(matches):,}"
    )

    ratings = {}

    rows = []

    print(
        "\nCalculando Elo..."
    )

    for _, match in matches.iterrows():

        home_team = match[
            "equipo_local"
        ]

        away_team = match[
            "equipo_visitante"
        ]

        home_elo = ratings.get(
            home_team,
            INITIAL_ELO
        )

        away_elo = ratings.get(
            away_team,
            INITIAL_ELO
        )

        rows.append({

            "match_idx":
                match["index"],

            "home_elo":
                round(home_elo, 2),

            "away_elo":
                round(away_elo, 2),

            "elo_diff":
                round(
                    home_elo
                    -
                    away_elo,
                    2
                )
        })

        result = get_match_result(
            match
        )

        new_home_elo, new_away_elo = (
            update_elo(
                home_elo,
                away_elo,
                result
            )
        )

        ratings[
            home_team
        ] = new_home_elo

        ratings[
            away_team
        ] = new_away_elo

    output = pd.DataFrame(
        rows
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

    print(
        "\nShape:"
    )

    print(
        output.shape
    )

    print(
        "\nResumen Elo:"
    )

    print(
        output[
            [
                "home_elo",
                "away_elo",
                "elo_diff"
            ]
        ].describe()
    )


if __name__ == "__main__":
    main()