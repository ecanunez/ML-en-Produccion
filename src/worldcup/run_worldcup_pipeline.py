import argparse
from time import perf_counter

from src.worldcup.scrape_fifa_teams import scrape_fifa_teams
from src.worldcup.scrape_worldcup_squads import scrape_worldcup_squads
from src.worldcup.build_worldcup_player_mapping import build_worldcup_player_mapping
from src.worldcup.build_worldcup_team_snapshot import build_worldcup_team_snapshot
from src.worldcup.enrich_worldcup_team_snapshot import enrich_worldcup_team_snapshot
from src.worldcup.scrape_fifa_ranking import scrape_fifa_ranking
from src.worldcup.scrape_worldcup_matches import scrape_worldcup_matches
from src.worldcup.build_worldcup_scoring_dataset import build_worldcup_scoring_dataset
from src.worldcup.predict_worldcup import predict_worldcup


PIPELINES = {
    "full": [
        ("FIFA Teams", scrape_fifa_teams),
        ("FIFA Squads", scrape_worldcup_squads),
        ("Player Mapping", build_worldcup_player_mapping),
        ("Team Snapshot", build_worldcup_team_snapshot),
        ("Enrich Snapshot", enrich_worldcup_team_snapshot),
        ("FIFA Ranking", scrape_fifa_ranking),
        ("World Cup Matches", scrape_worldcup_matches),
        ("Scoring Dataset", build_worldcup_scoring_dataset),
        ("Predictions", predict_worldcup),
    ],
    "refresh": [
        ("FIFA Ranking", scrape_fifa_ranking),
        ("World Cup Matches", scrape_worldcup_matches),
        ("Scoring Dataset", build_worldcup_scoring_dataset),
        ("Predictions", predict_worldcup),
    ],
    "predict": [
        ("Scoring Dataset", build_worldcup_scoring_dataset),
        ("Predictions", predict_worldcup),
    ],
}


def run_step(step_number, total_steps, name, function):
    print()
    print("=" * 70)
    print(f"{step_number}/{total_steps} - {name}")
    print("=" * 70)

    start = perf_counter()
    result = function()
    elapsed = perf_counter() - start

    print()
    print(f"✓ {name} finalizado ({elapsed:.1f} segundos)")

    return result


def run_worldcup_pipeline(mode="refresh"):
    if mode not in PIPELINES:
        raise ValueError(
            f"Modo inválido: {mode}. "
            f"Opciones válidas: {list(PIPELINES.keys())}"
        )

    steps = PIPELINES[mode]

    total_start = perf_counter()

    print()
    print("=" * 70)
    print("WORLD CUP PREDICTION PIPELINE")
    print("=" * 70)
    print(f"Modo: {mode}")
    print(f"Pasos: {len(steps)}")

    result = None

    for idx, (name, function) in enumerate(steps, start=1):
        result = run_step(
            step_number=idx,
            total_steps=len(steps),
            name=name,
            function=function,
        )

    total_elapsed = perf_counter() - total_start

    print()
    print("=" * 70)
    print("WORLD CUP PIPELINE FINALIZADO")
    print("=" * 70)
    print(f"Modo: {mode}")
    print(f"Tiempo total: {total_elapsed:.1f} segundos")

    if result is not None and hasattr(result, "__len__"):
        print(f"Filas resultado final: {len(result)}")

    print("Pipeline ejecutado correctamente.")

    return result


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ejecuta el pipeline de predicción del Mundial 2026."
    )

    parser.add_argument(
        "--mode",
        choices=list(PIPELINES.keys()),
        default="refresh",
        help=(
            "Modo de ejecución. "
            "'full' actualiza todo; "
            "'refresh' actualiza ranking/partidos y predice; "
            "'predict' solo reconstruye scoring y predice."
        ),
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_worldcup_pipeline(mode=args.mode)