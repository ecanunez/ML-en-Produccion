"""
Configuración global del proyecto.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

INTERIM_DATA_DIR = DATA_DIR / "interim"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = ROOT / "models"

REPORTS_DIR = ROOT / "src" / "reports"

BASE_URL = "https://www.transfermarkt.es"

PROJECT_VERSION = "v1.0"

MODEL_VERSION = (
    "v1.0_model_champion"
)

RANDOM_STATE = 42

TOP_FEATURES = 30

HISTORICAL_SEASONS = [
    2022,
    2023,
    2024,
    2025
]

SCORING_SEASON = 2026