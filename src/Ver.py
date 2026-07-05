from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

ROOT = Path(__file__).resolve().parents[1]

URL = "https://www.fifa.com/es/tournaments/mens/worldcup/canadamexicousa2026/teams/canada/team-news"

OUTPUT = ROOT / "data" / "prediction_worldcup" / "raw" / "fifa_canada_debug.html"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )

    try:
        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=90000
        )
    except TimeoutError:
        print("Timeout en goto, pero se intenta guardar el HTML cargado hasta ahora.")

    page.wait_for_timeout(10000)

    OUTPUT.write_text(
        page.content(),
        encoding="utf-8"
    )

    browser.close()

print(f"HTML guardado en: {OUTPUT}")