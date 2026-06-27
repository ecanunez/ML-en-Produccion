import os
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from src.scraper.scraper_utils import (
    extraer_datos_partido_internacional,
    obtener_enlaces_competicion,
)
from src.config.project_config import (
    HISTORICAL_SEASONS
)
from src.config.competition_config import (
    COMPETITIONS
)

BASE_URL = "https://www.transfermarkt.es"
SAVE_DIR = os.path.join("data", "raw", "games", "international_competitions")
os.makedirs(
    SAVE_DIR,
    exist_ok=True
)

url = construir_url_copa(
    competition,
    temporada
)

def seleccionar_competiciones():

    print("\n=== COMPETICIONES DISPONIBLES ===\n")

    for clave, comp in COMPETICIONES.items():

        print(
            f"{clave} - {comp['nombre']}"
        )

    print("\n0 - Todas")

    opcion = input(
        "\nSelecciona una o varias "
        "(ej: 1,3,4): "
    ).strip()

    if opcion == "0":

        return {
            v["nombre"]: {
                "slug": v["slug"],
                "id_web": v["id_web"]
            }
            for v in COMPETICIONES.values()
        }

    seleccionadas = {}

    for op in opcion.split(","):

        op = op.strip()

        if op in COMPETICIONES:

            comp = COMPETICIONES[op]

            seleccionadas[
                comp["nombre"]
            ] = {
                "slug": comp["slug"],
                "id_web": comp["id_web"]
            }

    return seleccionadas

def procesar_competicion(
    page,
    nombre_competicion,
    config
):

    for temporada in HISTORICAL_SEASONS:

        print(
            f"\nTemporada {temporada}"
        )

        partidos_temporada = []

        url = (
            f"{BASE_URL}/"
            f"{config['slug']}/"
            f"gesamtspielplan/"
            f"pokalwettbewerb/{config['id_web']}/"
            f"saison_id/{temporada}"
        )

        enlaces = obtener_enlaces_competicion(
            url,
            page
        )

        print(
            f"Partidos encontrados: "
            f"{len(enlaces)}"
        )

        for idx, enlace in enumerate(
            enlaces,
            start=1
        ):

            datos = (
                extraer_datos_partido_internacional(
                    enlace,
                    page,
                    nombre_competicion,
                    temporada,
                    "Internacional"
                )
            )

            if datos:
                partidos_temporada.append(
                    datos
                )

            if idx % 50 == 0:

                print(
                    f"Procesados "
                    f"{idx}/{len(enlaces)}"
                )

        guardar_competicion(
            nombre_competicion,
            temporada,
            partidos_temporada
        )

def guardar_competicion(
    nombre,
    temporada,
    partidos
):

    if not partidos:
        return

    df = pd.DataFrame(partidos)

    archivo = (
        nombre.lower()
        .replace(" ", "_")
        .replace("/", "_")
        + f"_{temporada}.csv"
    )

    ruta_salida = os.path.join(
        SAVE_DIR,
        archivo
    )

    df.to_csv(
        ruta_salida,
        index=False
    )

    print(
        f"Guardado: {ruta_salida}"
    )

# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    competiciones_a_procesar = (
        seleccionar_competiciones()
    )

    if not competiciones_a_procesar:

        print(
            "No se seleccionaron competiciones."
        )

        exit()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            viewport={
                "width": 1440,
                "height": 900
            }
        )

        page = context.new_page()

        try:

            for nombre, config in (
                competiciones_a_procesar.items()
            ):

                print("\n" + "=" * 50)
                print(
                    f"Procesando: {nombre}"
                )

                try:

                    procesar_competicion(
                        page,
                        nombre,
                        config
                    )

                except Exception as e:

                    print(
                        f"Error procesando "
                        f"{nombre}: {e}"
                    )

        finally:

            browser.close()

    print(
        "\nProceso finalizado."
    )