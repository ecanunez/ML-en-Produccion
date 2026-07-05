import requests
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
DEBUG_DIR = RAW_DIR / "debug_fifa_matches"

RAW_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_ALL = RAW_DIR / "fifa_worldcup_matches_all.parquet"
OUTPUT_UPCOMING = RAW_DIR / "fifa_worldcup_matches_upcoming.parquet"
OUTPUT_UPCOMING_CSV = RAW_DIR / "fifa_worldcup_matches_upcoming.csv"
DEBUG_JSON = DEBUG_DIR / "fifa_matches_api_response.json"

API_URL = (
    "https://api.fifa.com/api/v3/calendar/matches"
    "?language=es"
    "&count=500"
    "&idSeason=285023"
)


def scrape_worldcup_matches():
    print("Scrapeando partidos FIFA World Cup 2026")
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

    DEBUG_JSON.write_text(
        response.text,
        encoding="utf-8"
    )

    rows = []

    for match in data.get("Results", []):
        home = match.get("Home", {}) or {}
        away = match.get("Away", {}) or {}

        rows.append(
            {
                "match_id": match.get("IdMatch"),
                "match_date": match.get("Date"),
                "stage": match.get("StageName", [{}])[0].get("Description") if match.get("StageName") else None,
                "match_status": match.get("MatchStatus"),
                "result_type": match.get("ResultType"),

                "home_team": home.get("TeamName", [{}])[0].get("Description") if home.get("TeamName") else None,
                "home_fifa_code": home.get("Abbreviation"),
                "home_team_id": home.get("IdTeam"),
                "home_score": match.get("HomeTeamScore"),

                "away_team": away.get("TeamName", [{}])[0].get("Description") if away.get("TeamName") else None,
                "away_fifa_code": away.get("Abbreviation"),
                "away_team_id": away.get("IdTeam"),
                "away_score": match.get("AwayTeamScore"),

                "winner_team_id": match.get("Winner"),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df["match_date"] = pd.to_datetime(
            df["match_date"],
            errors="coerce",
            utc=True,
        )

        df = df.sort_values("match_date").reset_index(drop=True)

    # MatchStatus suele venir como:
    # 0 = jugado/finalizado
    # 1 = programado/no jugado
    upcoming = df[
        (df["match_status"] != 0)
        & (df["home_score"].isna())
        & (df["away_score"].isna())
    ].copy()

    df.to_parquet(OUTPUT_ALL, index=False)
    upcoming.to_parquet(OUTPUT_UPCOMING, index=False)
    upcoming.to_csv(OUTPUT_UPCOMING_CSV, index=False, encoding="utf-8-sig")

    print("\n============================================================")
    print("SCRAPE WORLD CUP MATCHES FINALIZADO")
    print("============================================================")
    print(f"Partidos totales: {len(df)}")
    print(f"Partidos pendientes: {len(upcoming)}")
    print("Archivos guardados:")
    print(OUTPUT_ALL)
    print(OUTPUT_UPCOMING)
    print(OUTPUT_UPCOMING_CSV)

    if not upcoming.empty:
        print("\nPróximos partidos:")
        print(
            upcoming[
                [
                    "match_date",
                    "stage",
                    "home_team",
                    "home_fifa_code",
                    "away_team",
                    "away_fifa_code",
                ]
            ].to_string(index=False)
        )

    return upcoming


if __name__ == "__main__":
    scrape_worldcup_matches()