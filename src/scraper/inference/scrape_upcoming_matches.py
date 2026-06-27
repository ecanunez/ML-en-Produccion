from pathlib import Path
from datetime import datetime
import pandas as pd
from playwright.sync_api import sync_playwright
from src.config.project_config import (
    SCORING_SEASON
)
from src.config.competition_config import (
    DOMESTIC_COMPETITIONS
)
from src.scraper.scraper_utils import (
    construir_url_fixture_liga,
    obtener_partidos_futuros,
    seleccionar_competiciones
)


OUTPUT_DIR = (
    Path("data")
    / "upcoming"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def main():

    partidos = []

    seleccion = seleccionar_competiciones()

    competiciones = seleccion["competiciones"]
    tipo_competicion = seleccion["tipo_competicion"]
    continentes_seleccionados = seleccion["continentes"]

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for competition in (competiciones.values()):

            print(f"\n{'=' * 60}")
            print(competition["nombre"])
            print(f"{'=' * 60}")

            url = construir_url_fixture_liga(
                competition,
                SCORING_SEASON
            )

            print(f"URL: {url}")

            partidos_competicion = (
                obtener_partidos_futuros(
                    url,
                    page
                )
            )

            for partido in partidos_competicion:

                partido["competition"] = (
                    competition["nombre"]
                )

                partido["continent"] = (
                    competition["continent"]
                )
                
                partido["season"] = (
                    SCORING_SEASON
                )

                partido["scrape_date"] = (
                    datetime.now().strftime("%Y-%m-%d")
                )

            partidos.extend(
                partidos_competicion
            )

            print(
                f"Partidos encontrados: "
                f"{len(partidos_competicion)}"
            )
        browser.close()

    df = pd.DataFrame(
        partidos
    )

    fecha = datetime.now().strftime("%Y%m%d")

    print(tipo_competicion)

    tipo_map = {
        "1": "domestic",
        "2": "international",
        "0": "all"
    }

    tipo_nombre = tipo_map[tipo_competicion]

    continentes_nombre = "-".join(
        c.lower().replace(" ", "_")
        for c in continentes_seleccionados
    )

    if not continentes_nombre:
        continentes_nombre = "allcontinents"

    filename = (
        f"upcoming_{tipo_nombre}_"
        f"{continentes_nombre}_"
        f"{fecha}.csv"
    )

    output_file = OUTPUT_DIR / filename

    df.to_csv(
        output_file,
        index=False
    )

    print("\nArchivo generado:")
    print(output_file)

    print(
        f"Total partidos: {len(df)}"
    )


if __name__ == "__main__":
    main()