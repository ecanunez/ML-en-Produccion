from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = ROOT / "data" / "raw"
INTERIM_DATA_DIR = ROOT / "data" / "interim"
PROCESSED_DATA_DIR = ROOT / "data" / "processed"
TOTALS_DIR = RAW_DATA_DIR / "games" / "totals"
INTL_DIR = RAW_DATA_DIR / "games" / "international_competitions"


PLAYER_MATCH_STATS_FILE = (
    "player_match_stats.parquet"
)

TEAM_STRENGTH_FILE = (
    "team_strength_features.parquet"
)

ELO_FEATURES_FILE = (
    "elo_features.parquet"
)

PLAYER_PROFILE_FILE = (
    "player_profile_features.parquet"
)

PLAYER_BALANCE_FILE = (
    "player_balance_features.parquet"
)

NEW_ELO_FILE = (
    "new_elo_features.parquet"
)

DRAW_FEATURES_FILE = (
    "draw_features.parquet"
)

INTERACTION_FEATURES_FILE = (
    "interaction_features.parquet"
)

FEATURE_FILES = [
    PLAYER_MATCH_STATS_FILE,
    TEAM_STRENGTH_FILE,
    ELO_FEATURES_FILE,
    PLAYER_PROFILE_FILE,
    PLAYER_BALANCE_FILE,
    NEW_ELO_FILE,
    DRAW_FEATURES_FILE,
    INTERACTION_FEATURES_FILE,
]