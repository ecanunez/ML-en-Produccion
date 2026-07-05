import re
import requests
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"
DEBUG_DIR = RAW_DIR / "debug_fifa_ranking"

RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

WORLD_CUP_TEAMS_PATH = RAW_DIR / "fifa_worldcup_teams.parquet"

OUTPUT_PATH = INTERIM_DIR / "worldcup_fifa_ranking.parquet"
OUTPUT_CSV_PATH = INTERIM_DIR / "worldcup_fifa_ranking.csv"
DEBUG_JSON_PATH = DEBUG_DIR / "fifa_ranking_api_response.json"

API_URL = (
    "https://inside.fifa.com/api/live-world-ranking/"
    "get-match-window-matches?locale=en&gender=1&rankingType=0"
)


def clean_text(value):
    if value is None:
        return None

    value = re.sub(r"\s+", " ", str(value)).strip()
    return value if value else None


def extract_team_name(team_obj):
    names = team_obj.get("TeamName", [])

    if names:
        return clean_text(names[0].get("Description"))

    return None


def scrape_fifa_ranking():
    print("Scrapeando ranking FIFA masculino")
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
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    DEBUG_JSON_PATH.write_text(
        response.text,
        encoding="utf-8"
    )

    rows = []

    for _, block in data.get("matches", {}).items():
        for match in block.get("MatchesList", []):
            match_date = match.get("Date")

            home = match.get("HomeTeam") or match.get("Home") or {}
            away = match.get("AwayTeam") or match.get("Away") or {}

            rows.append(
                {
                    "match_date": match_date,
                    "fifa_team_id": match.get("TeamAId"),
                    "ranking_team": extract_team_name(home),
                    "fifa_code": home.get("IdCountry"),
                    "fifa_ranking_points": match.get("TeamAPoints"),
                    "fifa_ranking_points_before": match.get("TeamAPointsBefore"),
                }
            )

            rows.append(
                {
                    "match_date": match_date,
                    "fifa_team_id": match.get("TeamBId"),
                    "ranking_team": extract_team_name(away),
                    "fifa_code": away.get("IdCountry"),
                    "fifa_ranking_points": match.get("TeamBPoints"),
                    "fifa_ranking_points_before": match.get("TeamBPointsBefore"),
                }
            )

    ranking_events = pd.DataFrame(rows)

    ranking_events["match_date"] = pd.to_datetime(
        ranking_events["match_date"],
        errors="coerce",
        utc=True
    )

    ranking_events["fifa_ranking_points"] = pd.to_numeric(
        ranking_events["fifa_ranking_points"],
        errors="coerce"
    )

    ranking_events["fifa_ranking_points_before"] = pd.to_numeric(
        ranking_events["fifa_ranking_points_before"],
        errors="coerce"
    )

    ranking_events = ranking_events.dropna(
        subset=["fifa_code", "fifa_ranking_points", "match_date"]
    )

    ranking_latest = (
        ranking_events
        .sort_values("match_date")
        .drop_duplicates(subset=["fifa_code"], keep="last")
        .reset_index(drop=True)
    )

    teams = pd.read_parquet(WORLD_CUP_TEAMS_PATH)

    worldcup_ranking = teams.merge(
        ranking_latest,
        on="fifa_code",
        how="left"
    )

    worldcup_ranking["ranking_matched"] = (
        worldcup_ranking["fifa_ranking_points"].notna()
    )

    worldcup_ranking["fifa_rank_proxy"] = (
        worldcup_ranking["fifa_ranking_points"]
        .rank(ascending=False, method="dense")
    )

    worldcup_ranking.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    worldcup_ranking.to_csv(
        OUTPUT_CSV_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n============================================================")
    print("FIFA RANKING WORLD CUP FINALIZADO")
    print("============================================================")
    print(f"Selecciones Mundial: {len(worldcup_ranking)}")
    print(f"Rankings encontrados: {worldcup_ranking['ranking_matched'].sum()}")
    print("Archivos guardados:")
    print(OUTPUT_PATH)
    print(OUTPUT_CSV_PATH)
    print(DEBUG_JSON_PATH)

    print("\nRanking faltante:")
    missing = worldcup_ranking.loc[
        ~worldcup_ranking["ranking_matched"],
        ["team", "fifa_code"]
    ]

    if missing.empty:
        print("Ninguno")
    else:
        print(missing.to_string(index=False))

    print("\nTop selecciones Mundial por puntos FIFA:")
    print(
        worldcup_ranking[
            [
                "team",
                "fifa_code",
                "fifa_rank_proxy",
                "fifa_ranking_points",
                "match_date",
            ]
        ]
        .sort_values("fifa_rank_proxy")
        .to_string(index=False)
    )

    return worldcup_ranking


if __name__ == "__main__":
    scrape_fifa_ranking()