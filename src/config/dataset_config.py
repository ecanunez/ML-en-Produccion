"""
Configuración del dataset.

Incluye:
- temporadas históricas
- temporada de scoring
- archivos que componen el dataset
"""

# --------------------------------------------------
# Features históricas
# --------------------------------------------------

FEATURE_FILES = [
    "player_match_stats.parquet",
    "team_strength_features.parquet",
    "elo_features.parquet",
    "player_profile_features.parquet",
    "player_balance_features.parquet",
    "new_elo_features.parquet",
    "draw_features.parquet",
    "interaction_features.parquet"
]

# --------------------------------------------------
# Temporadas utilizadas para entrenamiento
# --------------------------------------------------

HISTORICAL_SEASONS = [

    2022,
    2023,
    2024,
    2025

]

# --------------------------------------------------
# Temporada objetivo para scoring
# --------------------------------------------------

SCORING_SEASON = 2026