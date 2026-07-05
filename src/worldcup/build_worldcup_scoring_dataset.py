from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"
PROCESSED_DIR = ROOT / "data" / "prediction_worldcup" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MATCHES_PATH = RAW_DIR / "fifa_worldcup_matches_upcoming.parquet"
SNAPSHOT_PATH = INTERIM_DIR / "worldcup_team_snapshot_enriched.parquet"
RANKING_PATH = INTERIM_DIR / "worldcup_fifa_ranking.parquet"

OUTPUT_PATH = PROCESSED_DIR / "worldcup_scoring_dataset.parquet"
OUTPUT_CSV_PATH = PROCESSED_DIR / "worldcup_scoring_dataset.csv"


TOP30_FEATURES = [
    "elo_away_win_prob",
    "elo_home_win_prob",
    "elo_diff",
    "market_value_diff",
    "value_per_elo",
    "elo_market_interaction",
    "caps_diff",
    "DEF_value_diff",
    "home_avg_player_value",
    "caps_per_elo",
    "elo_caps_interaction",
    "away_avg_player_value",
    "away_team_market_value",
    "MID_value_diff",
    "elo_draw_proxy",
    "home_team_market_value",
    "elo_favorite_strength",
    "int_goals_diff",
    "abs_elo_diff",
    "home_avg_caps",
    "ATT_value_diff",
    "away_DEF_market_value_sum",
    "away_avg_caps",
    "abs_market_value_diff",
    "home_avg_age",
    "age_diff",
    "home_avg_int_goals",
    "abs_age_diff",
    "away_avg_age",
    "away_avg_height",
]


def elo_win_prob(elo_diff):
    return 1 / (1 + 10 ** (-elo_diff / 400))


def safe_divide(a, b):
    return np.where(
        np.abs(b) > 1e-9,
        a / b,
        0
    )


def build_worldcup_scoring_dataset():
    print("Leyendo partidos pendientes...")
    matches = pd.read_parquet(MATCHES_PATH)

    print("Leyendo snapshot enriquecido...")
    snapshot = pd.read_parquet(SNAPSHOT_PATH)

    print("Leyendo ranking FIFA...")
    ranking = pd.read_parquet(RANKING_PATH)

    # Solo partidos con equipos definidos
    matches = matches[
        matches["home_fifa_code"].notna()
        & matches["away_fifa_code"].notna()
    ].copy()

    print(f"Partidos con equipos definidos: {len(matches)}")

    # -----------------------------------------------------
    # Ranking como proxy Elo
    # -----------------------------------------------------

    ranking_cols = [
        "fifa_code",
        "fifa_ranking_points",
        "fifa_rank_proxy",
    ]

    ranking_small = ranking[ranking_cols].copy()

    snapshot = snapshot.merge(
        ranking_small,
        on="fifa_code",
        how="left"
    )

    snapshot = snapshot.rename(
        columns={
            "fifa_ranking_points": "team_elo",
            "fifa_rank_proxy": "fifa_rank_proxy",
        }
    )

    # -----------------------------------------------------
    # HOME / AWAY JOIN
    # -----------------------------------------------------

    home_snapshot = snapshot.add_prefix("home_")
    away_snapshot = snapshot.add_prefix("away_")

    df = matches.merge(
        home_snapshot,
        left_on="home_fifa_code",
        right_on="home_fifa_code",
        how="left"
    )

    df = df.merge(
        away_snapshot,
        left_on="away_fifa_code",
        right_on="away_fifa_code",
        how="left"
    )

    # -----------------------------------------------------
    # Features tipo Elo
    # -----------------------------------------------------

    df["home_elo"] = pd.to_numeric(df["home_team_elo"], errors="coerce")
    df["away_elo"] = pd.to_numeric(df["away_team_elo"], errors="coerce")

    df["elo_diff"] = df["home_elo"] - df["away_elo"]
    df["abs_elo_diff"] = df["elo_diff"].abs()

    df["elo_home_win_prob"] = elo_win_prob(df["elo_diff"])
    df["elo_away_win_prob"] = 1 - df["elo_home_win_prob"]

    df["elo_draw_proxy"] = 1 / (1 + df["abs_elo_diff"] / 100)
    df["elo_favorite_strength"] = df["abs_elo_diff"]

    # -----------------------------------------------------
    # Market value features
    # -----------------------------------------------------

    value_cols = [
        "home_team_market_value",
        "away_team_market_value",
        "home_avg_player_value",
        "away_avg_player_value",
        "home_GK_market_value_sum",
        "away_GK_market_value_sum",
        "home_DEF_market_value_sum",
        "away_DEF_market_value_sum",
        "home_MID_market_value_sum",
        "away_MID_market_value_sum",
        "home_ATT_market_value_sum",
        "away_ATT_market_value_sum",
    ]

    for col in value_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["market_value_diff"] = (
        df["home_team_market_value"]
        - df["away_team_market_value"]
    )

    df["abs_market_value_diff"] = df["market_value_diff"].abs()

    df["GK_value_diff"] = (
        df["home_GK_market_value_sum"]
        - df["away_GK_market_value_sum"]
    )

    df["DEF_value_diff"] = (
        df["home_DEF_market_value_sum"]
        - df["away_DEF_market_value_sum"]
    )

    df["MID_value_diff"] = (
        df["home_MID_market_value_sum"]
        - df["away_MID_market_value_sum"]
    )

    df["ATT_value_diff"] = (
        df["home_ATT_market_value_sum"]
        - df["away_ATT_market_value_sum"]
    )

    # -----------------------------------------------------
    # Profile diffs
    # -----------------------------------------------------

    profile_cols = [
        "home_avg_age",
        "away_avg_age",
        "home_avg_caps",
        "away_avg_caps",
        "home_avg_height",
        "away_avg_height",
        "home_avg_int_goals",
        "away_avg_int_goals",
    ]

    for col in profile_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["age_diff"] = df["home_avg_age"] - df["away_avg_age"]
    df["abs_age_diff"] = df["age_diff"].abs()

    df["caps_diff"] = df["home_avg_caps"] - df["away_avg_caps"]
    df["int_goals_diff"] = (
        df["home_avg_int_goals"]
        - df["away_avg_int_goals"]
    )

    # -----------------------------------------------------
    # Interaction features
    # -----------------------------------------------------

    df["value_per_elo"] = safe_divide(
        df["market_value_diff"],
        df["elo_diff"]
    )

    df["caps_per_elo"] = safe_divide(
        df["caps_diff"],
        df["elo_diff"]
    )

    df["elo_market_interaction"] = (
        df["elo_diff"]
        * df["market_value_diff"]
    )

    df["elo_caps_interaction"] = (
        df["elo_diff"]
        * df["caps_diff"]
    )

    # -----------------------------------------------------
    # Validación features
    # -----------------------------------------------------

    for feature in TOP30_FEATURES:
        if feature not in df.columns:
            df[feature] = 0

    df[TOP30_FEATURES] = df[TOP30_FEATURES].replace(
        [np.inf, -np.inf],
        0
    ).fillna(0)

    for col in df.columns:
        print(col)

    metadata_cols = [
        "match_id",
        "match_date",
        "stage",
        "home_team_x",
        "home_fifa_code",
        "away_team_x",
        "away_fifa_code",
    ]

    output = df[metadata_cols + TOP30_FEATURES].copy()

    output = output.rename(
        columns={
            "home_team_x": "home_team",
            "away_team_x": "away_team",
        }
    )

    output.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    output.to_csv(
        OUTPUT_CSV_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n============================================================")
    print("WORLD CUP SCORING DATASET FINALIZADO")
    print("============================================================")
    print(f"Partidos para predecir: {len(output)}")
    print(f"Features: {len(TOP30_FEATURES)}")
    print("Archivos guardados:")
    print(OUTPUT_PATH)
    print(OUTPUT_CSV_PATH)

    print("\nPartidos incluidos:")
    print(
        output[
            [
                "match_date",
                "stage",
                "home_team",
                "away_team",
            ]
        ].to_string(index=False)
    )

    return output


if __name__ == "__main__":
    build_worldcup_scoring_dataset()