from pathlib import Path

import joblib
import pandas as pd
import shutil


ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT / "models" / "champions" / "v1.0_model_champion" / "model.joblib"
TOP30_PATH = ROOT / "src" / "reports" / "top30_features.csv"

SCORING_PATH = (
    ROOT
    / "data"
    / "prediction_worldcup"
    / "processed"
    / "worldcup_scoring_dataset.parquet"
)

PREDICTIONS_DIR = ROOT / "data" / "prediction_worldcup" / "predictions"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = PREDICTIONS_DIR / "worldcup_predictions.parquet"
OUTPUT_CSV_PATH = PREDICTIONS_DIR / "worldcup_predictions.csv"

DRAW_THRESHOLD = 0.54

def backup_existing_predictions():
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

    backup_dir = PREDICTIONS_DIR / "backups"
    backup_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    files_to_backup = [
        OUTPUT_PATH,
        OUTPUT_CSV_PATH,
    ]

    for file_path in files_to_backup:

        if not file_path.exists():
            continue

        backup_path = (
            backup_dir
            / f"{file_path.stem}_{timestamp}{file_path.suffix}"
        )

        shutil.copy2(
            file_path,
            backup_path,
        )

        print(f"Backup creado: {backup_path}")


def load_expected_features(model):
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    top30 = pd.read_csv(TOP30_PATH)

    if "feature" in top30.columns:
        return top30["feature"].tolist()

    return top30.iloc[:, 0].tolist()


def apply_draw_threshold_rule(row):
    if row["prob_draw"] >= DRAW_THRESHOLD:
        return "DRAW"

    return "HOME" if row["prob_home"] >= row["prob_away"] else "AWAY"


def predict_worldcup():
    print("Cargando modelo campeón...")
    model = joblib.load(MODEL_PATH)
    expected_features = load_expected_features(model)

    print("Leyendo dataset de scoring...")
    scoring = pd.read_parquet(SCORING_PATH)

    missing_features = [
        feature for feature in expected_features
        if feature not in scoring.columns
    ]

    if missing_features:
        raise ValueError(
            "Faltan features en el scoring dataset: "
            f"{missing_features}"
        )

    X = scoring[expected_features].copy()

    print(f"Partidos a predecir: {len(X)}")
    print(f"Features utilizadas: {X.shape[1]}")

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    classes = list(model.classes_)

    proba_df = pd.DataFrame(
        probabilities,
        columns=[f"prob_{cls.lower()}" for cls in classes],
    )

    output = pd.concat(
        [
            scoring[
                [
                    "match_id",
                    "match_date",
                    "stage",
                    "home_team",
                    "home_fifa_code",
                    "away_team",
                    "away_fifa_code",
                ]
            ].reset_index(drop=True),
            pd.Series(predictions, name="prediction_original"),
            proba_df,
        ],
        axis=1,
    )

    output["prediction_adjusted"] = output.apply(
        apply_draw_threshold_rule,
        axis=1,
    )

    output["prediction"] = output["prediction_adjusted"]

    ordered_cols = [
        "match_id",
        "match_date",
        "stage",
        "home_team",
        "home_fifa_code",
        "away_team",
        "away_fifa_code",
        "prediction",
        "prediction_original",
        "prediction_adjusted",
        "prob_away",
        "prob_draw",
        "prob_home",
    ]

    output = output[ordered_cols]
    
    backup_existing_predictions()

    output.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    output.to_csv(
        OUTPUT_CSV_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n============================================================")
    print("WORLD CUP PREDICTIONS FINALIZADAS")
    print("============================================================")
    print(f"Predicciones: {len(output)}")
    print(f"Draw threshold aplicado: {DRAW_THRESHOLD}")
    print("Archivos guardados:")
    print(OUTPUT_PATH)
    print(OUTPUT_CSV_PATH)

    print("\nPredicciones:")
    display_cols = [
        "match_date",
        "stage",
        "home_team",
        "away_team",
        "prediction",
        "prediction_original",
        "prob_away",
        "prob_draw",
        "prob_home",
    ]

    print(output[display_cols].to_string(index=False))

    # =========================================================
    # RESUMEN PREDICCIONES
    # =========================================================

    summary = output.copy()

    summary["partido"] = (
        summary["home_team"]
        + " vs "
        + summary["away_team"]
    )


    def prediction_to_team(row):
        if row["prediction"] == "HOME":
            return row["home_team"]

        if row["prediction"] == "AWAY":
            return row["away_team"]

        return "Empate"


    summary["predicción"] = summary.apply(
        prediction_to_team,
        axis=1,
    )

    summary["confianza"] = summary.apply(
        lambda row: {
            "HOME": row["prob_home"],
            "DRAW": row["prob_draw"],
            "AWAY": row["prob_away"],
        }[row["prediction"]],
        axis=1,
    )

    summary["confianza"] = (
        summary["confianza"]
        .map(lambda x: f"{x*100:.1f}%")
    )

    summary = summary.sort_values("match_date")

    summary = summary[
        [
            "stage",
            "partido",
            "predicción",
            "confianza",
        ]
    ]

    summary = summary.rename(
        columns={
            "stage": "fase",
        }
    )

    print("\n============================================================")
    print("PREDICCIONES DEL MUNDIAL")
    print("============================================================\n")

    print(summary.to_string(index=False))

    return output


if __name__ == "__main__":
    predict_worldcup()