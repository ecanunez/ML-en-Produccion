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
    / "interim"
    / "player_balance_features.parquet"
)


def main():

    print("Leyendo dataset...")

    df = pd.read_parquet(
        INPUT_FILE
    )

    features = pd.DataFrame()

    features["match_idx"] = df["match_idx"]

    # ==========================================
    # Balance experiencia internacional
    # ==========================================

    features["abs_caps_diff"] = (
        df["caps_diff"]
        .abs()
    )

    features["abs_age_diff"] = (
        df["age_diff"]
        .abs()
    )

    features["abs_int_goals_diff"] = (
        df["int_goals_diff"]
        .abs()
    )

    # ==========================================
    # Balance valor de mercado
    # ==========================================

    features["abs_market_value_diff"] = (
        df["market_value_diff"]
        .abs()
    )

    features["abs_GK_value_diff"] = (
        df["GK_value_diff"]
        .abs()
    )

    features["abs_DEF_value_diff"] = (
        df["DEF_value_diff"]
        .abs()
    )

    features["abs_MID_value_diff"] = (
        df["MID_value_diff"]
        .abs()
    )

    features["abs_ATT_value_diff"] = (
        df["ATT_value_diff"]
        .abs()
    )

    # ==========================================
    # Balance deportivo
    # ==========================================

    features["abs_elo_diff"] = (
        df["elo_diff"]
        .abs()
    )

    features["abs_points_diff"] = (
        df["points_diff"]
        .abs()
    )

    features["abs_gd_diff"] = (
        df["gd_diff"]
        .abs()
    )

    # ==========================================
    # Indicadores de equilibrio
    # ==========================================

    features["elo_balanced"] = (
        features["abs_elo_diff"] < 50
    ).astype(int)

    features["market_balanced"] = (
        features["abs_market_value_diff"] < 30_000_000
    ).astype(int)

    features["caps_balanced"] = (
        features["abs_caps_diff"] < 10
    ).astype(int)

    features["age_balanced"] = (
        features["abs_age_diff"] < 2
    ).astype(int)

    # ==========================================
    # Score global de equilibrio
    # ==========================================

    features["balance_score"] = (
        features["elo_balanced"]
        + features["market_balanced"]
        + features["caps_balanced"]
        + features["age_balanced"]
    )

    features["high_balance_match"] = (
        features["balance_score"] >= 3
    ).astype(int)

    # ==========================================
    # Guardado
    # ==========================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    features.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nArchivo generado:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        f"\nShape: {features.shape}"
    )

    print(
        "\nVariables creadas:"
    )

    for col in features.columns:
        if col != "match_idx":
            print(f" - {col}")


if __name__ == "__main__":
    main()