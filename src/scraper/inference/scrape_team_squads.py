from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright
from src.scraper.scraper_utils import (
    extraer_plantilla_equipo,
    buscar_url_equipo_transfermarkt
)
from src.config.project_config import (
    RAW_DATA_DIR,
)

UPCOMING_DIR = (
    RAW_DATA_DIR
    / "upcoming_matches"
)

OUTPUT_DIR = (
    RAW_DATA_DIR
    / "team_squads"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def obtener_ultimo_upcoming():

    archivos = sorted(
        UPCOMING_DIR.glob("upcoming_*.csv")
    )

    if not archivos:
        raise FileNotFoundError(
            "No hay archivos upcoming."
        )

    return archivos[-1]


def main():

    upcoming_file = obtener_ultimo_upcoming()

    print(
        f"\nLeyendo: {upcoming_file}"
    )

    df = pd.read_csv(
        upcoming_file
    )

    equipos = set(
        df["local"].dropna()
    )

    equipos.update(
        df["visitante"].dropna()
    )

    equipos = sorted(equipos)

    print(
        f"Equipos únicos: {len(equipos)}"
    )

    todos_jugadores = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for equipo in equipos:

            try:

                # print(
                #     f"\nScrapeando {equipo}"
                # )

                url = (
                    buscar_url_equipo_transfermarkt(
                        equipo,
                        page
                    )
                )

                if not url:

                    print(
                        f"No encontrado: {equipo}"
                    )

                    continue

                jugadores = (
                    extraer_plantilla_equipo(
                        equipo,
                        url,
                        page
                    )
                )

                todos_jugadores.extend(
                    jugadores
                )

            except Exception as e:

                print(
                    f"Error {equipo}: {e}"
                )

        browser.close()

    df_players = pd.DataFrame(
        todos_jugadores
    )

    output_file = (
        OUTPUT_DIR
        / f"team_squads_{pd.Timestamp.now():%Y%m%d}.csv"
    )

    df_players.to_csv(
        output_file,
        index=False
    )

    print("\nArchivo generado:")
    print(output_file)

    print(
        f"Jugadores: {len(df_players)}"
    )


if __name__ == "__main__":
    main()