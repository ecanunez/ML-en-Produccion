"""
competition_config.py

Configuración centralizada de competiciones utilizadas
en el proyecto ML-en-Produccion.

region:
    - domestic
    - international

continent:
    - Europe
    - South America
    - North America
    - Asia
    - Africa
"""

COMPETITIONS = {

    # =====================================================
    # INTERNACIONALES
    # =====================================================

    "champions_league": {
        "nombre": "Champions League",
        "slug": "uefa-champions-league",
        "id_web": "CL",
        "region": "international",
        "continent": "Europe"
    },

    "europa_league": {
        "nombre": "Europa League",
        "slug": "uefa-europa-league",
        "id_web": "EL",
        "region": "international",
        "continent": "Europe"
    },

    "libertadores": {
        "nombre": "Copa Libertadores",
        "slug": "copa-libertadores",
        "id_web": "LIBC",
        "region": "international",
        "continent": "South America"
    },

    "sudamericana": {
        "nombre": "Copa Sudamericana",
        "slug": "copa-sudamericana",
        "id_web": "COSU",
        "region": "international",
        "continent": "South America"
    },

    "concacaf_champions": {
        "nombre": "Concacaf Champions Cup",
        "slug": "concacaf-champions-cup",
        "id_web": "CCC",
        "region": "international",
        "continent": "North America"
    },

    "afc_champions": {
        "nombre": "AFC Champions League",
        "slug": "afc-champions-league",
        "id_web": "AFCL",
        "region": "international",
        "continent": "Asia"
    },

    "caf_champions": {
        "nombre": "CAF Champions League",
        "slug": "caf-champions-league",
        "id_web": "CAFCL",
        "region": "international",
        "continent": "Africa"
    },

    # =====================================================
    # EUROPA
    # =====================================================

    "laliga": {
        "nombre": "LaLiga",
        "slug": "laliga",
        "id_web": "ES1",
        "region": "domestic",
        "continent": "Europe"
    },

    "premier_league": {
        "nombre": "Premier League",
        "slug": "premier-league",
        "id_web": "GB1",
        "region": "domestic",
        "continent": "Europe"
    },

    "bundesliga": {
        "nombre": "Bundesliga",
        "slug": "bundesliga",
        "id_web": "L1",
        "region": "domestic",
        "continent": "Europe"
    },

    "serie_a": {
        "nombre": "Serie A",
        "slug": "serie-a",
        "id_web": "IT1",
        "region": "domestic",
        "continent": "Europe"
    },

    "ligue_1": {
        "nombre": "Ligue 1",
        "slug": "ligue-1",
        "id_web": "FR1",
        "region": "domestic",
        "continent": "Europe"
    },

    "primeira_liga": {
        "nombre": "Primeira Liga",
        "slug": "liga-nos",
        "id_web": "PO1",
        "region": "domestic",
        "continent": "Europe"
    },

    "eredivisie": {
        "nombre": "Eredivisie",
        "slug": "eredivisie",
        "id_web": "NL1",
        "region": "domestic",
        "continent": "Europe"
    },

    "jupiler_pro_league": {
        "nombre": "Jupiler Pro League",
        "slug": "jupiler-pro-league",
        "id_web": "BE1",
        "region": "domestic",
        "continent": "Europe"
    },

    "super_lig": {
        "nombre": "Süper Lig",
        "slug": "super-lig",
        "id_web": "TR1",
        "region": "domestic",
        "continent": "Europe"
    },

    "chance_liga": {
        "nombre": "Chance Liga",
        "slug": "chance-liga",
        "id_web": "CZ1",
        "region": "domestic",
        "continent": "Europe"
    },

    # =====================================================
    # SUDAMÉRICA
    # =====================================================

    "brasileirao": {
        "nombre": "Brasileirao",
        "slug": "campeonato-brasileiro-serie-a",
        "id_web": "BRA1",
        "region": "domestic",
        "continent": "South America"
    },

    "argentina_primera": {
        "nombre": "Liga Profesional Argentina",
        "slug": "liga-profesional-de-futbol",
        "id_web": "AR1N",
        "region": "domestic",
        "continent": "South America"
    },

    "bolivia_primera": {
        "nombre": "Bolivia División Profesional",
        "slug": "division-profesional",
        "id_web": "BODP",
        "region": "domestic",
        "continent": "South America"
    },

    "chile_primera": {
        "nombre": "Chile Primera División",
        "slug": "primera-division",
        "id_web": "CLPD",
        "region": "domestic",
        "continent": "South America"
    },

    "colombia_primera": {
        "nombre": "Colombia Primera A",
        "slug": "primera-a",
        "id_web": "COAA",
        "region": "domestic",
        "continent": "South America"
    },

    "ecuador_ligapro": {
        "nombre": "Ecuador LigaPro",
        "slug": "ligapro",
        "id_web": "ECP1",
        "region": "domestic",
        "continent": "South America"
    },

    "paraguay_primera": {
        "nombre": "Paraguay Primera División",
        "slug": "primera-division",
        "id_web": "PAR1",
        "region": "domestic",
        "continent": "South America"
    },

    "peru_liga1": {
        "nombre": "Perú Liga 1",
        "slug": "liga-1",
        "id_web": "PEL1",
        "region": "domestic",
        "continent": "South America"
    },

    "uruguay_primera": {
        "nombre": "Uruguay Primera División",
        "slug": "primera-division",
        "id_web": "URU1",
        "region": "domestic",
        "continent": "South America"
    },

    "venezuela_primera": {
        "nombre": "Venezuela Primera División",
        "slug": "primera-division",
        "id_web": "VFP1",
        "region": "domestic",
        "continent": "South America"
    },

    # =====================================================
    # NORTEAMÉRICA
    # =====================================================

    "mls": {
        "nombre": "Major League Soccer",
        "slug": "major-league-soccer",
        "id_web": "MLS1",
        "region": "domestic",
        "continent": "North America"
    },

    "liga_mx": {
        "nombre": "Liga MX",
        "slug": "liga-mx-clausura",
        "id_web": "MEX1",
        "region": "domestic",
        "continent": "North America"
    },

    # =====================================================
    # ASIA
    # =====================================================

    "saudi_pro_league": {
        "nombre": "Saudi Pro League",
        "slug": "saudi-pro-league",
        "id_web": "SA1",
        "region": "domestic",
        "continent": "Asia"
    },

    "j1_league": {
        "nombre": "J1 League",
        "slug": "j1-league",
        "id_web": "JAP1",
        "region": "domestic",
        "continent": "Asia"
    },

    "k_league_1": {
        "nombre": "K-League 1",
        "slug": "k-league-1",
        "id_web": "KOR1",
        "region": "domestic",
        "continent": "Asia"
    },

    # =====================================================
    # ÁFRICA
    # =====================================================

    "egypt_premier_league": {
        "nombre": "Egipto Premier League",
        "slug": "egyptian-premier-league",
        "id_web": "EGY1",
        "region": "domestic",
        "continent": "Africa"
    },

    "botola_pro": {
        "nombre": "Botola Pro",
        "slug": "botola-pro",
        "id_web": "MAR1",
        "region": "domestic",
        "continent": "Africa"
    },

    "tunisia_ligue_1": {
        "nombre": "Túnez Ligue 1",
        "slug": "ligue-1-professionnelle-1",
        "id_web": "TUN1",
        "region": "domestic",
        "continent": "Africa"
    },

    "linafoot": {
        "nombre": "Linafoot",
        "slug": "linafoot",
        "id_web": "COD1",
        "region": "domestic",
        "continent": "Africa"
    }
}

def get_competitions_by_region(region):

    return {
        k: v
        for k, v in COMPETITIONS.items()
        if v["region"] == region
    }


def get_competitions_by_continent(continent):

    return {
        k: v
        for k, v in COMPETITIONS.items()
        if v["continent"] == continent
    }


# =====================================================
# ATAJOS DE USO FRECUENTE
# =====================================================

INTERNATIONAL_COMPETITIONS = (
    get_competitions_by_region(
        "international"
    )
)

DOMESTIC_COMPETITIONS = (
    get_competitions_by_region(
        "domestic"
    )
)