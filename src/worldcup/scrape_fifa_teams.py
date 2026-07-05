import re
import requests
from pathlib import Path

import pandas as pd


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
DEBUG_DIR = RAW_DIR / "debug_fifa_teams"

RAW_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = RAW_DIR / "fifa_worldcup_teams.parquet"
OUTPUT_CSV_PATH = RAW_DIR / "fifa_worldcup_teams.csv"
DEBUG_JSON_PATH = DEBUG_DIR / "fifa_teams_api_response.json"


# =========================================================
# CONFIG
# =========================================================

BASE_URL = "https://www.fifa.com"

API_URL = (
    "https://cxm-api.fifa.com/fifaplusweb/api/sections/"
    "teamsModule/4v5Yng3VdGD9c1cpnOIff1?locale=es&limit=200"
)


# =========================================================
# HELPERS
# =========================================================

def clean_text(value):
    if value is None:
        return None

    value = re.sub(r"\s+", " ", str(value)).strip()
    return value if value else None


def normalize_url(href):
    if not href:
        return None

    if href.startswith("/"):
        return BASE_URL + href

    return href


def extract_slug_from_url(url):
    if not url:
        return None

    match = re.search(r"/teams/([^/]+)", url)

    if match:
        return match.group(1)

    return None


def extract_fifa_code_from_flag_url(url):
    if not url:
        return None

    match = re.search(r"/flags-\{format\}-\{size\}/([A-Z]{2,3})", url)

    if match:
        return match.group(1)

    return None


# =========================================================
# SCRAPER
# =========================================================

def scrape_fifa_teams():
    print("Scrapeando selecciones desde API FIFA")
    print(API_URL)

    response = requests.get(
        API_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    DEBUG_JSON_PATH.write_text(
        response.text,
        encoding="utf-8"
    )

    teams = []

    for item in data.get("teams", []):
        team_name = clean_text(item.get("teamName"))
        team_id = item.get("teamId")
        confederation = item.get("confederationId")
        team_page_url = item.get("teamPageUrl")
        team_flag = item.get("teamFlag")

        team_url = normalize_url(team_page_url)
        fifa_slug = extract_slug_from_url(team_url)
        fifa_code = extract_fifa_code_from_flag_url(team_flag)

        squad_url = None
        if team_url:
            squad_url = team_url.rstrip("/") + "/squad"

        teams.append(
            {
                "team": team_name,
                "fifa_team_id": team_id,
                "fifa_slug": fifa_slug,
                "fifa_code": fifa_code,
                "confederation": confederation,
                "team_url": team_url,
                "squad_url": squad_url,
                "source_url": API_URL,
            }
        )

    df = pd.DataFrame(teams)

    if not df.empty:
        df = (
            df.dropna(subset=["fifa_slug"])
              .drop_duplicates(subset=["fifa_slug"])
              .sort_values("team")
              .reset_index(drop=True)
        )

    df.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    df.to_csv(
        OUTPUT_CSV_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n============================================================")
    print("SCRAPE FIFA WORLD CUP TEAMS FINALIZADO")
    print("============================================================")
    print(f"Selecciones encontradas: {len(df)}")
    print("Archivos guardados en:")
    print(OUTPUT_PATH)
    print(OUTPUT_CSV_PATH)
    print(DEBUG_JSON_PATH)

    if len(df) != 48:
        print("\nATENCIÓN: se esperaban 48 selecciones.")
        print("Revisar fifa_teams_api_response.json")

    return df


if __name__ == "__main__":
    scrape_fifa_teams()