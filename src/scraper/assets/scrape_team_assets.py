from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright

from src.scraper.scraper_utils import (
    buscar_url_equipo_transfermarkt,
    extraer_logo_equipo,
)

from src.config.project_config import (
    RAW_DATA_DIR,
)


UPCOMING_DIR = (
    RAW_DATA_DIR
    / "upcoming_matches"
)

ASSETS_DIR = (
    RAW_DATA_DIR.parent
    / "assets"
)

OUTPUT_FILE = (
    ASSETS_DIR
    / "team_assets.csv"
)

ASSETS_DIR.mkdir(
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


def cargar_assets_existentes():

    if OUTPUT_FILE.exists():

        return pd.read_csv(
            OUTPUT_FILE
        )

    return pd.DataFrame(
        columns=[
            "team_name",
            "team_url",
            "logo_url",
        ]
    )


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

    assets_df = cargar_assets_existentes()

    equipos_existentes = set(
        assets_df["team_name"]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
    )

    equipos_faltantes = [
        equipo
        for equipo in equipos
        if equipo.lower().strip() not in equipos_existentes
    ]

    print(
        f"Assets existentes: {len(equipos_existentes)}"
    )

    print(
        f"Assets faltantes: {len(equipos_faltantes)}"
    )

    registros = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for equipo in equipos_faltantes:

            try:

                print(
                    f"\nProcesando: {equipo}"
                )

                url = buscar_url_equipo_transfermarkt(
                    equipo,
                    page,
                )

                if not url:

                    print(
                        f"  No encontrado: {equipo}"
                    )

                    continue

                logo_url = extraer_logo_equipo(
                    url,
                    page,
                )

                if not logo_url:

                    print(
                        f"  Logo no encontrado: {equipo}"
                    )

                    continue

                registros.append(
                    {
                        "team_name": equipo,
                        "team_url": url,
                        "logo_url": logo_url,
                    }
                )

                print(
                    f"  Logo encontrado: {logo_url}"
                )

            except Exception as e:

                print(
                    f"  Error {equipo}: {e}"
                )

        browser.close()

    if registros:

        nuevos_df = pd.DataFrame(
            registros
        )

        output_df = pd.concat(
            [
                assets_df,
                nuevos_df,
            ],
            ignore_index=True,
        )

        output_df = output_df.drop_duplicates(
            subset=["team_name"],
            keep="last",
        )

        output_df.to_csv(
            OUTPUT_FILE,
            index=False,
        )

        print(
            f"\nArchivo actualizado: {OUTPUT_FILE}"
        )

        print(
            f"Nuevos assets: {len(nuevos_df)}"
        )

    else:

        print(
            "\nNo se agregaron nuevos assets."
        )


if __name__ == "__main__":

    main()