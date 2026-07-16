from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright

from src.config.project_config import RAW_DATA_DIR
from src.scraper.scraper_utils import (
    buscar_url_equipo_transfermarkt,
    extraer_logo_equipo,
)


# =========================================================
# PATHS
# =========================================================

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
    exist_ok=True,
)


# =========================================================
# HELPERS
# =========================================================

def obtener_ultimo_upcoming() -> Path:
    archivos = sorted(
        UPCOMING_DIR.glob("upcoming_*.csv")
    )

    if not archivos:
        raise FileNotFoundError(
            f"No hay archivos upcoming en: {UPCOMING_DIR}"
        )

    return archivos[-1]


def cargar_assets_existentes() -> pd.DataFrame:
    if OUTPUT_FILE.exists():
        assets_df = pd.read_csv(
            OUTPUT_FILE
        )

        if "team_name" not in assets_df.columns:
            raise ValueError(
                "team_assets.csv no contiene la columna 'team_name'."
            )

        return assets_df

    return pd.DataFrame(
        columns=[
            "team_name",
            "team_url",
            "logo_url",
        ]
    )


def normalizar_nombre_equipo(nombre: str) -> str:
    return (
        str(nombre)
        .strip()
        .lower()
    )


def obtener_equipos(df: pd.DataFrame) -> list[str]:
    required_columns = {
        "local",
        "visitante",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Faltan columnas en el archivo upcoming: "
            f"{sorted(missing_columns)}"
        )

    equipos = set(
        df["local"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    equipos.update(
        df["visitante"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    equipos.discard("")

    return sorted(equipos)


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    upcoming_file = obtener_ultimo_upcoming()

    print(
        f"\nLeyendo: {upcoming_file}"
    )

    df = pd.read_csv(
        upcoming_file
    )

    equipos = obtener_equipos(
        df
    )

    print(
        f"Equipos únicos: {len(equipos)}"
    )

    assets_df = cargar_assets_existentes()

    equipos_existentes = set(
        assets_df["team_name"]
        .dropna()
        .astype(str)
        .map(normalizar_nombre_equipo)
        .tolist()
    )

    equipos_faltantes = [
        equipo
        for equipo in equipos
        if normalizar_nombre_equipo(equipo)
        not in equipos_existentes
    ]

    print(
        f"Assets existentes: {len(equipos_existentes)}"
    )

    print(
        f"Assets faltantes: {len(equipos_faltantes)}"
    )

    if not equipos_faltantes:
        print(
            "\nNo hay nuevos assets para procesar."
        )
        return

    registros = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        try:
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

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=60000,
                    )

                    page.wait_for_timeout(
                        1500
                    )

                    logo_url = extraer_logo_equipo(
                        page
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

                except KeyboardInterrupt:
                    print(
                        "\nProceso interrumpido por el usuario."
                    )
                    break

                except Exception as e:
                    print(
                        f"  Error {equipo}: {e}"
                    )

        finally:
            browser.close()

    if not registros:
        print(
            "\nNo se agregaron nuevos assets."
        )
        return

    nuevos_df = pd.DataFrame(
        registros
    )

    output_df = pd.concat(
        [
            assets_df,
            nuevos_df,
        ],
        ignore_index=True,
        sort=False,
    )

    output_df = output_df.drop_duplicates(
        subset=["team_name"],
        keep="last",
    )

    output_df = output_df.sort_values(
        "team_name"
    ).reset_index(
        drop=True
    )

    output_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print(
        f"\nArchivo actualizado: {OUTPUT_FILE}"
    )

    print(
        f"Nuevos assets: {len(nuevos_df)}"
    )

    print(
        f"Assets totales: {len(output_df)}"
    )


if __name__ == "__main__":
    main()