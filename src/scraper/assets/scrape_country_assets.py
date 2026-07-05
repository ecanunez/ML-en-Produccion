import time
from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright

from src.scraper.scraper_utils import (
    buscar_url_equipo_transfermarkt,
    extraer_logo_equipo,
)


# =========================================================
# PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[3]

WORLDCUP_TEAMS_PATH = (
    ROOT_DIR
    / "data"
    / "prediction_worldcup"
    / "raw"
    / "fifa_worldcup_teams.csv"
)

ASSETS_DIR = (
    ROOT_DIR
    / "data"
    / "assets"
)

METADATA_PATH = (
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

def normalize_name(name):
    return (
        str(name)
        .strip()
        .lower()
    )


def load_worldcup_teams():

    if not WORLDCUP_TEAMS_PATH.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {WORLDCUP_TEAMS_PATH}"
        )

    df = pd.read_csv(
        WORLDCUP_TEAMS_PATH
    )

    if "team" not in df.columns:
        raise ValueError(
            "El archivo fifa_worldcup_teams.csv no tiene columna 'team'."
        )

    teams = (
        df["team"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return teams


def load_existing_assets():

    if METADATA_PATH.exists():
        return pd.read_csv(
            METADATA_PATH
        )

    return pd.DataFrame(
        columns=[
            "team_name",
            "asset_type",
            "team_url",
            "logo_url",
            "source_url",
            "local_path",
        ]
    )


def get_existing_team_names(assets_df):

    if assets_df.empty:
        return set()

    return set(
        assets_df["team_name"]
        .dropna()
        .astype(str)
        .map(normalize_name)
        .tolist()
    )


# =========================================================
# MAIN
# =========================================================

def scrape_country_assets():

    print("\nLeyendo selecciones del Mundial...")
    print(WORLDCUP_TEAMS_PATH)

    teams = load_worldcup_teams()

    print(
        f"Selecciones detectadas: {len(teams)}"
    )

    assets_df = load_existing_assets()

    existing_teams = get_existing_team_names(
        assets_df
    )

    missing_teams = [
        team
        for team in teams
        if normalize_name(team) not in existing_teams
    ]

    print(
        f"Assets existentes: {len(existing_teams)}"
    )

    print(
        f"Assets faltantes: {len(missing_teams)}"
    )

    records = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        for team_name in missing_teams:

            try:

                print(
                    f"\nProcesando: {team_name}"
                )

                team_url = buscar_url_equipo_transfermarkt(
                    team_name,
                    page,
                )

                if not team_url:

                    print(
                        f"  No encontrado en Transfermarkt: {team_name}"
                    )

                    continue

                page.goto(
                    team_url,
                    wait_until="networkidle",
                    timeout=60000,
                )

                page.wait_for_timeout(
                    2000
                )

                logo_url = extraer_logo_equipo(
                    page
                )

                if not logo_url:

                    print(
                        f"  Logo no encontrado: {team_name}"
                    )

                    continue

                records.append(
                    {
                        "team_name": team_name,
                        "asset_type": "country",
                        "team_url": team_url,
                        "logo_url": logo_url,
                        "source_url": logo_url,
                        "local_path": "",
                    }
                )

                print(
                    f"  Logo encontrado: {logo_url}"
                )

                time.sleep(
                    1
                )

            except Exception as e:

                print(
                    f"  Error con {team_name}: {e}"
                )

        browser.close()

    if records:

        new_df = pd.DataFrame(
            records
        )

        output_df = pd.concat(
            [
                assets_df,
                new_df,
            ],
            ignore_index=True,
        )

        output_df = output_df.drop_duplicates(
            subset=["team_name"],
            keep="last",
        )

        output_df.to_csv(
            METADATA_PATH,
            index=False,
            encoding="utf-8",
        )

        print()
        print(
            f"Metadata actualizada: {METADATA_PATH}"
        )

        print(
            f"Nuevos assets agregados: {len(new_df)}"
        )

    else:

        print()
        print(
            "No se agregaron nuevos assets."
        )


if __name__ == "__main__":

    scrape_country_assets()