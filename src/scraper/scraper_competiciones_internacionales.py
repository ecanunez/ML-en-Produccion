import os
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from funciones import extraer_datos_partido_internacional
from funciones import obtener_enlaces_competicion

BASE_URL = "https://www.transfermarkt.es"

TEMPORADAS = [
    #2022, 2023, 2024, 
    2025]


COMPETICIONES = {
    "Champions League": {
        "slug": "uefa-champions-league",
        "id_web": "CL"
    }
    #,
    #     "Europa League": {
    #         "slug": "europa-league",
    #         "id_web": "EL"
    #     },
    #     "Copa Libertadores": {
    #         "slug": "copa-libertadores",
    #         "id_web": "LIBC"
    #     },
    #     "Copa Sudamericana": {
    #         "slug": "copa-sudamericana",
    #         "id_web": "COSU"
    #     },
    #     "Concacaf Champions Cup": {
    #         "slug": "concacaf-champions-cup",
    #         "id_web": "CCC"
    #     },
    #     "AFC Champions League": {
    #        "slug": "afc-champions-league",
    #         "id_web": "AFCL"
    #     },
    #     "CAF Champions League": {
    #         "slug": "caf-champions-league",
    #         "id_web": "CAFCL"
    #     }
}

def procesar_competicion(
    page,
    nombre_competicion,
    config
):

    todos_los_partidos = []

    for temporada in TEMPORADAS:

        print(
            f"\nTemporada {temporada}"
        )

        url = (
            f"{BASE_URL}/"
            f"{config['slug']}/"
            f"gesamtspielplan/"
            f"pokalwettbewerb/{config['id_web']}/"
            f"saison_id/{temporada}"
        )

        print(url)

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

            datos = extraer_datos_partido_internacional(
                enlace,
                page,
                nombre_competicion,
                temporada,
                "Internacional"
            )

            if datos:
                todos_los_partidos.append(
                    datos
                )

            if idx % 50 == 0:

                print(
                    f"Procesados "
                    f"{idx}/{len(enlaces)}"
                )

    return todos_los_partidos

def guardar_competicion(nombre, partidos):

    if not partidos:
        return

    df = pd.DataFrame(partidos)

    archivo = (
        nombre.lower()
        .replace(" ", "_")
        + ".csv"
    )

    df.to_csv(
        archivo,
        index=False
    )

    print(f"Guardado: {archivo}")


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

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

        for nombre, config in COMPETICIONES.items():

            print("\n" + "=" * 50)
            print(f"Procesando: {nombre}")

            partidos = procesar_competicion(
                page,
                nombre,
                config
            )

            guardar_competicion(
                nombre,
                partidos
            )

        browser.close()