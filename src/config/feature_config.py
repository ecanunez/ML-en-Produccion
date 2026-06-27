"""
Configuración del pipeline de features.
"""

# --------------------------------------------------
# Columnas a eliminar antes del entrenamiento
# --------------------------------------------------

DROP_COLUMNS = [

    "region",
    "liga",
    "temporada",
    "fecha",
    "fecha_partido",

    "equipo_local",
    "equipo_visitante",

    "resultado",

    "source_file",

    "goles_local",
    "goles_visitante"

]

DROP_COLUMNS += [
    f"local_jugador_{i}"
    for i in range(1, 12)
]

DROP_COLUMNS += [
    f"visitante_jugador_{i}"
    for i in range(1, 12)
]

# --------------------------------------------------
# Columnas excluidas del entrenamiento
# --------------------------------------------------

BASE_EXCLUDED_COLUMNS = [
    "match_idx",
    "target"
]

ENGINEERED_COLUMNS_TO_DROP = [

    "home_elo",
    "away_elo",

    "home_team_market_value_mean",
    "away_team_market_value_mean",

    "home_GK_market_value_mean",
    "away_GK_market_value_mean",

    "home_DEF_market_value_mean",
    "away_DEF_market_value_mean",

    "home_MID_market_value_mean",
    "away_MID_market_value_mean",

    "home_ATT_market_value_mean",
    "away_ATT_market_value_mean"

]

EXCLUDED_COLUMNS = (
    BASE_EXCLUDED_COLUMNS
    + ENGINEERED_COLUMNS_TO_DROP
)

# --------------------------------------------------
# Entrenamiento
# --------------------------------------------------

RANDOM_STATE = 42