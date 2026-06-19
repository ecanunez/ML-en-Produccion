from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "training_dataset.parquet"
)

OUTPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "training_dataset_v2.parquet"
)


def main():

    print("Leyendo dataset...")

    df = pd.read_parquet(INPUT_FILE)

    print(f"Observaciones: {len(df):,}")
    print(f"Columnas originales: {len(df.columns)}")

    # =====================================================
    # DIFERENCIAS OFENSIVAS / DEFENSIVAS
    # =====================================================

    df["gf_diff"] = (
        df["home_gf_last5"]
        - df["away_gf_last5"]
    )

    df["ga_diff"] = (
        df["home_ga_last5"]
        - df["away_ga_last5"]
    )

    # =====================================================
    # CALIDAD DE COBERTURA DE PLANTILLA
    # =====================================================

    df["players_found_diff"] = (
        df["home_players_found"]
        - df["away_players_found"]
    )

    # =====================================================
    # RATIOS
    # =====================================================

    eps = 1.0

    df["market_value_ratio"] = (
        df["home_team_market_value"]
        /
        (df["away_team_market_value"] + eps)
    )

    # Opcional: evitar valores extremos
    df["market_value_ratio"] = (
        df["market_value_ratio"]
        .clip(lower=0, upper=20)
    )

    print(f"Columnas finales: {len(df.columns)}")

    new_features = [
        "gf_diff",
        "ga_diff",
        "players_found_diff",
        "market_value_ratio",
    ]

    print("\nFeatures creadas:")
    for feature in new_features:
        print(f" - {feature}")

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nDataset guardado en:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()