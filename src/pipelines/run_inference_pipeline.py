import subprocess
import sys


STEPS = [
    (
        "Scrapear próximos partidos",
        "src.scraper.inference.scrape_upcoming_matches"
    ),
    (
        "Scrapear plantillas de equipos",
        "src.scraper.inference.scrape_team_squads"
    ),
    (
        "Construir team_features",
        "src.features.inference.build_team_features"
    ),
    (
        "Construir team_player_features",
        "src.features.inference.build_player_features"
    ),
    (
        "Construir dataset de inferencia",
        "src.scoring.build_scoring_dataset"
    ),
    (
        "Generar predicciones",
        "src.inference.predict"
    ),
]


def run_step(description, module_name):

    print("\n" + "=" * 80)
    print(description)
    print("=" * 80)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module_name
        ],
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Falló el paso: {description}"
        )


def main():

    print("\n" + "=" * 80)
    print("PIPELINE DE INFERENCIA")
    print("=" * 80)

    for description, module_name in STEPS:
        run_step(
            description,
            module_name
        )

    print("\n" + "=" * 80)
    print("PIPELINE DE INFERENCIA COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    main()