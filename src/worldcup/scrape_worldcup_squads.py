import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError
from src.config.worldcup_config import BASE_URL

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
DEBUG_DIR = RAW_DIR / "debug_fifa_squads"

RAW_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = RAW_DIR / "fifa_worldcup_squads.parquet"
TEAMS_PATH = RAW_DIR / "fifa_worldcup_teams.parquet"

# =========================================================
# HELPERS
# =========================================================

def clean_text(value):
    if value is None:
        return None

    value = re.sub(r"\s+", " ", str(value)).strip()
    return value if value else None


def build_squad_url(fifa_slug):
    return f"{BASE_URL}/{fifa_slug}/squad"


def parse_player_card_text(text):
    text = clean_text(text)

    if not text:
        return None, None

    positions = [
        "Arquero",
        "Defensor",
        "Mediocampista",
        "Delantero"
    ]

    position = None

    for pos in positions:
        if pos in text:
            position = pos
            text = text.replace(pos, " ")

    text = clean_text(text)

    if not text:
        return None, None

    if not position:
        return None, None

    parts = text.split(" ")

    half = len(parts) // 2

    if len(parts) % 2 == 0 and parts[:half] == parts[half:]:
        player_name = " ".join(parts[:half])
    else:
        player_name = text

    player_name = clean_text(player_name)

    return player_name, position


def extract_players_from_html(
    html,
    team,
    fifa_slug,
    fifa_code,
    confederation,
    source_url
):
    soup = BeautifulSoup(html, "html.parser")

    possible_cards = soup.select(
        "a[href*='/players/'], "
        "a[href*='/player/'], "
        "div[class*='player'], "
        "article[class*='player']"
    )

    players = []
    seen = set()

    for card in possible_cards:
        text = clean_text(card.get_text(" ", strip=True))

        if not text or len(text) > 120:
            continue

        player_name, position = parse_player_card_text(text)

        if not player_name or not position:
            continue

        key = (team, player_name, position)

        if key in seen:
            continue

        seen.add(key)

        href = None

        if card.name == "a":
            href = card.get("href")
        else:
            link = card.select_one("a[href]")
            if link:
                href = link.get("href")

        player_url = None

        if href:
            player_url = href
            if href.startswith("/"):
                player_url = "https://www.fifa.com" + href

        players.append(
            {
                "team": team,
                "confederation": confederation,
                "fifa_slug": fifa_slug,
                "fifa_code": fifa_code,
                "player_name": player_name,
                "position": position,
                "player_name_raw": text,
                "player_url": player_url,
                "source_url": source_url,
            }
        )

    return players


def scrape_team_squad(page, team_config):
    team = team_config["team"]
    fifa_slug = team_config["fifa_slug"]
    fifa_code = team_config["fifa_code"]
    confederation = team_config.get("confederation")

    url = build_squad_url(fifa_slug)

    print(f"\nScrapeando plantilla FIFA: {team}")
    print(url)

    try:
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=90000
        )
    except TimeoutError:
        print("Timeout en goto, se intenta continuar con el HTML cargado.")

    page.wait_for_timeout(10000)

    html = page.content()

    debug_path = DEBUG_DIR / f"{fifa_slug}_squad.html"
    debug_path.write_text(html, encoding="utf-8")

    players = extract_players_from_html(
        html=html,
        team=team,
        fifa_slug=fifa_slug,
        fifa_code=fifa_code,
        confederation=confederation,
        source_url=url
    )

    print(f"Jugadores extraídos: {len(players)}")
    print(f"HTML debug: {debug_path}")

    return players


# =========================================================
# MAIN
# =========================================================

def scrape_worldcup_squads():
    all_players = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        teams_df = pd.read_parquet(TEAMS_PATH)
        teams = teams_df.to_dict("records")

        for team_config in teams:
            players = scrape_team_squad(
                page=page,
                team_config=team_config
            )

            all_players.extend(players)

        browser.close()

    df = pd.DataFrame(all_players)

    df.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print("\n============================================================")
    print("SCRAPE FIFA WORLD CUP SQUADS FINALIZADO")
    print("============================================================")
    print(f"Selecciones: {df['team'].nunique() if not df.empty else 0}")
    print(f"Jugadores: {len(df)}")
    print(f"Archivo guardado en:")
    print(OUTPUT_PATH)

    return df


if __name__ == "__main__":
    scrape_worldcup_squads()