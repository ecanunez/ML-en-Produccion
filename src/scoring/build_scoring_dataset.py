from datetime import datetime
import shutil

import joblib
import pandas as pd

from src.config.project_config import (
    RAW_DATA_DIR,
    MODELS_DIR,
    PROCESSED_DATA_DIR,
)


UPCOMING_MATCHES_DIR = (
    RAW_DATA_DIR
    / "upcoming_matches"
)

TEAM_FEATURES_DIR = (
    PROCESSED_DATA_DIR
    / "team_features"
)

TEAM_PLAYER_FEATURES_DIR = (
    PROCESSED_DATA_DIR
    / "team_player_features"
)

BACKUP_DIR = (
    PROCESSED_DATA_DIR
    / "backups"
)

SCORING_DATASET_CSV = (
    PROCESSED_DATA_DIR
    / "scoring_dataset.csv"
)

SCORING_DATASET_PARQUET = (
    PROCESSED_DATA_DIR
    / "scoring_dataset.parquet"
)

MODEL_FILE = (
    MODELS_DIR
    / "champion_model.pkl"
)

BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def get_latest_file(directory, pattern):

    files = list(
        directory.glob(pattern)
    )

    if not files:
        raise FileNotFoundError(
            f"No se encontraron archivos {pattern} en {directory}"
        )

    return max(
        files,
        key=lambda x: x.stat().st_mtime
    )


def backup_existing_file(file_path):

    if not file_path.exists():
        return

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        BACKUP_DIR
        / f"{file_path.stem}_{timestamp}{file_path.suffix}"
    )

    shutil.copy2(
        file_path,
        backup_file
    )

    print(
        f"Backup generado: {backup_file}"
    )


def detect_team_columns(df):

    candidates = [
        ("home_team", "away_team"),
        ("equipo_local", "equipo_visitante"),
        ("local_team", "away_team"),
        ("team_home", "team_away"),
        ("home", "away"),
        ("local", "visitante"),
    ]

    for home_col, away_col in candidates:

        if home_col in df.columns and away_col in df.columns:

            return home_col, away_col

    print("\nColumnas disponibles:")
    print(df.columns.tolist())

    raise ValueError(
        "No se pudieron detectar columnas de equipo local y visitante."
    )


def add_prefix(df, prefix):

    cols_to_rename = {
        col: f"{prefix}_{col}"
        for col in df.columns
    }

    return df.rename(
        columns=cols_to_rename
    )


def main():

    print("\nConstruyendo scoring dataset...")

    artifact = joblib.load(
        MODEL_FILE
    )

    expected_features = artifact["features"]

    upcoming_file = get_latest_file(
        UPCOMING_MATCHES_DIR,
        "upcoming_*.csv"
    )

    team_features_file = get_latest_file(
        TEAM_FEATURES_DIR,
        "team_features_*.csv"
    )

    player_features_file = get_latest_file(
        TEAM_PLAYER_FEATURES_DIR,
        "team_player_features_*.csv"
    )

    print(f"\nUpcoming matches:\n{upcoming_file}")
    print(f"\nTeam features:\n{team_features_file}")
    print(f"\nPlayer features:\n{player_features_file}")

    matches = pd.read_csv(
        upcoming_file
    )

    print("\nColumnas upcoming:")
    print(matches.columns.tolist())

    team_features = pd.read_csv(
        team_features_file
    )

    player_features = pd.read_csv(
        player_features_file
    )

    home_col, away_col = detect_team_columns(
        matches
    )

    matches = matches.rename(
        columns={
            home_col: "home_team",
            away_col: "away_team"
        }
    )

    team_all = team_features.merge(
        player_features,
        on="team",
        how="left"
    )

    home_features = add_prefix(
        team_all,
        "home"
    )

    away_features = add_prefix(
        team_all,
        "away"
    )

    df = matches.merge(
        home_features,
        left_on="home_team",
        right_on="home_team",
        how="left"
    )

    df = df.merge(
        away_features,
        left_on="away_team",
        right_on="away_team",
        how="left"
    )

    # --------------------------------------------------
    # Diferencias base
    # --------------------------------------------------

    if {
        "home_team_market_value",
        "away_team_market_value"
    }.issubset(df.columns):

        df["market_value_diff"] = (
            df["home_team_market_value"]
            - df["away_team_market_value"]
        )

        df["abs_market_value_diff"] = (
            df["market_value_diff"]
            .abs()
        )

    if {
        "home_def_market_value",
        "away_def_market_value"
    }.issubset(df.columns):

        df["DEF_value_diff"] = (
            df["home_def_market_value"]
            - df["away_def_market_value"]
        )

    if {
        "home_mid_market_value",
        "away_mid_market_value"
    }.issubset(df.columns):

        df["MID_value_diff"] = (
            df["home_mid_market_value"]
            - df["away_mid_market_value"]
        )

    if {
        "home_att_market_value",
        "away_att_market_value"
    }.issubset(df.columns):

        df["ATT_value_diff"] = (
            df["home_att_market_value"]
            - df["away_att_market_value"]
        )

    if {
        "home_avg_caps",
        "away_avg_caps"
    }.issubset(df.columns):

        df["caps_diff"] = (
            df["home_avg_caps"]
            - df["away_avg_caps"]
        )

    if {
        "home_avg_int_goals",
        "away_avg_int_goals"
    }.issubset(df.columns):

        df["int_goals_diff"] = (
            df["home_avg_int_goals"]
            - df["away_avg_int_goals"]
        )

    if {
        "home_avg_age",
        "away_avg_age"
    }.issubset(df.columns):

        df["age_diff"] = (
            df["home_avg_age"]
            - df["away_avg_age"]
        )

        df["abs_age_diff"] = (
            df["age_diff"]
            .abs()
        )

    # --------------------------------------------------
    # ELO neutral placeholder
    # --------------------------------------------------

    elo_defaults = {
        "elo_diff": 0.0,
        "abs_elo_diff": 0.0,
        "elo_home_win_prob": 0.5,
        "elo_away_win_prob": 0.5,
        "elo_draw_proxy": 1.0,
        "elo_favorite_strength": 0.0,
        "value_per_elo": 0.0,
        "caps_per_elo": 0.0,
        "elo_market_interaction": 0.0,
        "elo_caps_interaction": 0.0,
    }

    for col, value in elo_defaults.items():

        if col not in df.columns:
            df[col] = value

    # --------------------------------------------------
    # Validar features esperadas por el modelo
    # --------------------------------------------------

    missing_features = [
        col
        for col in expected_features
        if col not in df.columns
    ]

    if missing_features:

        print("\nFeatures faltantes. Se completan con 0:")

        for col in missing_features:
            print(f" - {col}")
            df[col] = 0.0

    df[expected_features] = (
        df[expected_features]
        .fillna(0)
    )

    # --------------------------------------------------
    # Backup + guardado
    # --------------------------------------------------

    backup_existing_file(
        SCORING_DATASET_CSV
    )

    backup_existing_file(
        SCORING_DATASET_PARQUET
    )

    df.to_csv(
        SCORING_DATASET_CSV,
        index=False
    )

    df.to_parquet(
        SCORING_DATASET_PARQUET,
        index=False
    )

    print("\nScoring dataset generado:")
    print(SCORING_DATASET_CSV)
    print(SCORING_DATASET_PARQUET)

    print(f"\nPartidos: {len(df)}")
    print(f"Features modelo: {len(expected_features)}")


if __name__ == "__main__":
    main()