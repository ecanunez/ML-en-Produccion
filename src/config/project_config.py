"""
Configuración global del proyecto.
Contiene únicamente rutas y parámetros generales.
"""

from pathlib import Path

# --------------------------------------------------
# Proyecto
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

PROJECT_VERSION = "v1.0"

BASE_URL = "https://www.transfermarkt.es"

# --------------------------------------------------
# Directorios principales
# --------------------------------------------------

DATA_DIR = ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

INTERIM_DATA_DIR = DATA_DIR / "interim"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = ROOT / "models"

REPORTS_DIR = ROOT / "src" / "reports"

# --------------------------------------------------
# Subdirectorios
# --------------------------------------------------

RAW_GAMES_DIR = RAW_DATA_DIR / "games"

TOTALS_DIR = RAW_GAMES_DIR / "totals"

INTL_DIR = RAW_GAMES_DIR / "international_competitions"

PLAYERS_DIR = RAW_DATA_DIR / "players"

TEAM_SQUADS_DIR = RAW_DATA_DIR / "team_squads"

UPCOMING_MATCHES_DIR = RAW_DATA_DIR / "upcoming_matches"

PROCESSED_FEATURES_DIR = PROCESSED_DATA_DIR