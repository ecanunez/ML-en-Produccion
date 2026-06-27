import subprocess
import sys


STEPS = [
    (
        "Consolidar partidos históricos",
        "src.data.consolidacion"
    ),
    (
        "Construir matches.parquet",
        "src.data.build_matches"
    ),
    (
        "Construir player_mapping.parquet",
        "src.data.build_player_mapping"
    ),
    (
        "Construir player_match_stats",
        "src.features.engineering.build_player_match_stats"
    ),
    (
        "Construir team_strength_features",
        "src.features.engineering.build_team_strength_features"
    ),
    (
        "Construir elo_features",
        "src.features.engineering.build_elo_features"
    ),
    (
        "Construir player_profile_features",
        "src.features.engineering.build_player_profile_features"
    ),
    (
        "Construir training_dataset base",
        "src.data.build_training_dataset"
    ),
    (
        "Construir player_balance_features",
        "src.features.engineering.build_player_balance_features"
    ),
    (
        "Construir new_elo_features",
        "src.features.engineering.create_new_elo_features"
    ),
    (
        "Construir draw_features",
        "src.features.engineering.create_draw_features"
    ),
    (
        "Construir interaction_features",
        "src.features.engineering.create_interaction_features"
    ),
    (
        "Reconstruir training_dataset final",
        "src.data.build_training_dataset"
    ),
    (
        "Entrenar modelo",
        "src.models.train"
    ),
    (
        "Exportar modelo campeón",
        "src.models.export_champion_model"
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
    print("PIPELINE HISTÓRICO")
    print("=" * 80)

    for description, module_name in STEPS:
        run_step(
            description,
            module_name
        )

    print("\n" + "=" * 80)
    print("PIPELINE HISTÓRICO COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    main()