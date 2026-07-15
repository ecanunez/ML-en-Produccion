import json
import requests
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "prediction_worldcup" / "raw"
INTERIM_DIR = ROOT / "data" / "prediction_worldcup" / "interim"
REPORTS_DIR = ROOT / "data" / "prediction_worldcup" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

MATCHES_PATH = RAW_DIR / "fifa_worldcup_matches_all.parquet"
SNAPSHOT_PATH = INTERIM_DIR / "worldcup_team_snapshot_enriched.parquet"

MODEL_PATH = ROOT / "models" / "champions" / "v1.0_model_champion" / "model.joblib"
TOP30_PATH = ROOT / "src" / "reports" / "top30_features.csv"

OUTPUT_PREDICTIONS = (
    REPORTS_DIR / "worldcup_evaluation_predictions.csv"
)

OUTPUT_METRICS = (
    REPORTS_DIR / "worldcup_evaluation_metrics.json"
)

OUTPUT_CONFUSION = (
    REPORTS_DIR / "worldcup_evaluation_confusion_matrix.csv"
)

OUTPUT_RULE_SEARCH = (
    REPORTS_DIR / "worldcup_decision_rule_search.csv"
)

OUTPUT_CLASSIFICATION_REPORT = (
    REPORTS_DIR / "worldcup_evaluation_classification_report.csv"
)


RANKING_API_URL = (
    "https://inside.fifa.com/api/live-world-ranking/"
    "get-match-window-matches?locale=en&gender=1&rankingType=0"
)


def elo_win_prob(elo_diff):
    return 1 / (1 + 10 ** (-elo_diff / 400))


def safe_divide(a, b):
    return np.where(np.abs(b) > 1e-9, a / b, 0)


def load_expected_features(model):
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    top30 = pd.read_csv(TOP30_PATH)

    if "feature" in top30.columns:
        return top30["feature"].tolist()

    return top30.iloc[:, 0].tolist()


def get_match_ranking_points_before():
    response = requests.get(
        RANKING_API_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
        timeout=60,
    )

    response.raise_for_status()
    data = response.json()

    rows = []

    for _, block in data.get("matches", {}).items():
        for match in block.get("MatchesList", []):
            home = match.get("HomeTeam") or match.get("Home") or {}
            away = match.get("AwayTeam") or match.get("Away") or {}

            rows.append(
                {
                    "match_id": match.get("IdMatch"),
                    "home_fifa_code": home.get("IdCountry"),
                    "away_fifa_code": away.get("IdCountry"),
                    "home_elo_before": match.get("TeamAPointsBefore"),
                    "away_elo_before": match.get("TeamBPointsBefore"),
                }
            )

    ranking = pd.DataFrame(rows)

    ranking["home_elo_before"] = pd.to_numeric(
        ranking["home_elo_before"],
        errors="coerce",
    )

    ranking["away_elo_before"] = pd.to_numeric(
        ranking["away_elo_before"],
        errors="coerce",
    )

    return ranking.drop_duplicates("match_id")


def build_actual_result(row):
    if row["home_score"] > row["away_score"]:
        return "HOME"

    if row["home_score"] < row["away_score"]:
        return "AWAY"

    return "DRAW"


def apply_draw_margin_rule(row, margin):
    probs = {
        "AWAY": row["prob_away"],
        "DRAW": row["prob_draw"],
        "HOME": row["prob_home"],
    }

    winner = max(probs, key=probs.get)

    if winner != "DRAW":
        return winner

    best_non_draw = "HOME" if probs["HOME"] >= probs["AWAY"] else "AWAY"

    if probs["DRAW"] - probs[best_non_draw] <= margin:
        return best_non_draw

    return "DRAW"


def apply_draw_threshold_rule(row, threshold):
    if row["prob_draw"] >= threshold:
        return "DRAW"

    return "HOME" if row["prob_home"] >= row["prob_away"] else "AWAY"


def evaluate_rule(y_true, y_pred, rule_name, param_value=None):
    return {
        "rule": rule_name,
        "param": param_value,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }


def evaluate_worldcup():
    print("Cargando modelo campeón...")
    model = joblib.load(MODEL_PATH)
    expected_features = load_expected_features(model)

    print("Leyendo partidos del Mundial...")
    matches = pd.read_parquet(MATCHES_PATH)

    print("Leyendo snapshot enriquecido...")
    snapshot = pd.read_parquet(SNAPSHOT_PATH)

    print("Leyendo puntos FIFA pre-partido...")
    ranking_before = get_match_ranking_points_before()

    played = matches[
        (matches["match_status"] == 0)
        & matches["home_fifa_code"].notna()
        & matches["away_fifa_code"].notna()
        & matches["home_score"].notna()
        & matches["away_score"].notna()
    ].copy()

    played["home_score"] = pd.to_numeric(played["home_score"], errors="coerce")
    played["away_score"] = pd.to_numeric(played["away_score"], errors="coerce")
    played["actual_result"] = played.apply(build_actual_result, axis=1)

    played = played.merge(
        ranking_before,
        on=["match_id", "home_fifa_code", "away_fifa_code"],
        how="left",
    )

    home_snapshot = snapshot.add_prefix("home_")
    away_snapshot = snapshot.add_prefix("away_")

    df = played.merge(
        home_snapshot,
        left_on="home_fifa_code",
        right_on="home_fifa_code",
        how="left",
    )

    df = df.merge(
        away_snapshot,
        left_on="away_fifa_code",
        right_on="away_fifa_code",
        how="left",
    )

    df["home_elo"] = pd.to_numeric(df["home_elo_before"], errors="coerce")
    df["away_elo"] = pd.to_numeric(df["away_elo_before"], errors="coerce")

    df = df.dropna(subset=["home_elo", "away_elo"]).copy()

    df["elo_diff"] = df["home_elo"] - df["away_elo"]
    df["abs_elo_diff"] = df["elo_diff"].abs()
    df["elo_home_win_prob"] = elo_win_prob(df["elo_diff"])
    df["elo_away_win_prob"] = 1 - df["elo_home_win_prob"]
    df["elo_draw_proxy"] = 1 / (1 + df["abs_elo_diff"] / 100)
    df["elo_favorite_strength"] = df["abs_elo_diff"]

    numeric_cols = [
        "home_team_market_value",
        "away_team_market_value",
        "home_avg_player_value",
        "away_avg_player_value",
        "home_GK_market_value_sum",
        "away_GK_market_value_sum",
        "home_DEF_market_value_sum",
        "away_DEF_market_value_sum",
        "home_MID_market_value_sum",
        "away_MID_market_value_sum",
        "home_ATT_market_value_sum",
        "away_ATT_market_value_sum",
        "home_avg_age",
        "away_avg_age",
        "home_avg_caps",
        "away_avg_caps",
        "home_avg_height",
        "away_avg_height",
        "home_avg_int_goals",
        "away_avg_int_goals",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["market_value_diff"] = (
        df["home_team_market_value"]
        - df["away_team_market_value"]
    )
    df["abs_market_value_diff"] = df["market_value_diff"].abs()

    df["GK_value_diff"] = (
        df["home_GK_market_value_sum"]
        - df["away_GK_market_value_sum"]
    )

    df["DEF_value_diff"] = (
        df["home_DEF_market_value_sum"]
        - df["away_DEF_market_value_sum"]
    )

    df["MID_value_diff"] = (
        df["home_MID_market_value_sum"]
        - df["away_MID_market_value_sum"]
    )

    df["ATT_value_diff"] = (
        df["home_ATT_market_value_sum"]
        - df["away_ATT_market_value_sum"]
    )

    df["age_diff"] = df["home_avg_age"] - df["away_avg_age"]
    df["abs_age_diff"] = df["age_diff"].abs()

    df["caps_diff"] = df["home_avg_caps"] - df["away_avg_caps"]

    df["int_goals_diff"] = (
        df["home_avg_int_goals"]
        - df["away_avg_int_goals"]
    )

    df["value_per_elo"] = safe_divide(
        df["market_value_diff"],
        df["elo_diff"],
    )

    df["caps_per_elo"] = safe_divide(
        df["caps_diff"],
        df["elo_diff"],
    )

    df["elo_market_interaction"] = (
        df["elo_diff"]
        * df["market_value_diff"]
    )

    df["elo_caps_interaction"] = (
        df["elo_diff"]
        * df["caps_diff"]
    )

    for feature in expected_features:
        if feature not in df.columns:
            df[feature] = 0

    X = (
        df[expected_features]
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    classes = list(model.classes_)

    proba_df = pd.DataFrame(
        probabilities,
        columns=[f"prob_{cls.lower()}" for cls in classes],
    )

    output = pd.concat(
        [
            df[
                [
                    "match_id",
                    "match_date",
                    "stage",
                    "home_team_x",
                    "home_fifa_code",
                    "home_score",
                    "away_team_x",
                    "away_fifa_code",
                    "away_score",
                    "actual_result",
                ]
            ].reset_index(drop=True),
            pd.Series(predictions, name="prediction"),
            proba_df,
        ],
        axis=1,
    )

    output = output.rename(
        columns={
            "home_team_x": "home_team",
            "away_team_x": "away_team",
        }
    )

    y_true = output["actual_result"]

    results = []

    results.append(
        evaluate_rule(
            y_true=y_true,
            y_pred=output["prediction"],
            rule_name="original",
            param_value=None,
        )
    )

    for margin in np.arange(0.00, 0.151, 0.01):
        margin = round(float(margin), 2)
        pred_col = f"prediction_draw_margin_{margin:.2f}"

        output[pred_col] = output.apply(
            apply_draw_margin_rule,
            axis=1,
            margin=margin,
        )

        results.append(
            evaluate_rule(
                y_true=y_true,
                y_pred=output[pred_col],
                rule_name="draw_margin",
                param_value=margin,
            )
        )

    for threshold in np.arange(0.45, 0.701, 0.01):
        threshold = round(float(threshold), 2)
        pred_col = f"prediction_draw_threshold_{threshold:.2f}"

        output[pred_col] = output.apply(
            apply_draw_threshold_rule,
            axis=1,
            threshold=threshold,
        )

        results.append(
            evaluate_rule(
                y_true=y_true,
                y_pred=output[pred_col],
                rule_name="draw_threshold",
                param_value=threshold,
            )
        )

    results_df = pd.DataFrame(results)

    best_row = results_df.sort_values(
        ["f1_macro", "accuracy"],
        ascending=False,
    ).iloc[0]

    best_rule = best_row["rule"]
    best_param = best_row["param"]

    if best_rule == "original":
        best_prediction_col = "prediction"
    else:
        best_prediction_col = f"prediction_{best_rule}_{best_param:.2f}"

    output["prediction_adjusted"] = output[best_prediction_col]

    metrics = {
        "matches_evaluated": int(len(output)),
        "original_accuracy": float(
            results_df.loc[
                results_df["rule"] == "original",
                "accuracy",
            ].iloc[0]
        ),
        "original_f1_macro": float(
            results_df.loc[
                results_df["rule"] == "original",
                "f1_macro",
            ].iloc[0]
        ),
        "best_rule": str(best_rule),
        "best_param": None if pd.isna(best_param) else float(best_param),
        "best_accuracy": float(best_row["accuracy"]),
        "best_f1_macro": float(best_row["f1_macro"]),
        "labels": classes,
    }

    cm = pd.DataFrame(
        confusion_matrix(
            y_true,
            output["prediction_adjusted"],
            labels=classes,
        ),
        index=[f"actual_{c}" for c in classes],
        columns=[f"pred_{c}" for c in classes],
    )

    report_df = pd.DataFrame(
        classification_report(
            y_true,
            output["prediction_adjusted"],
            labels=classes,
            zero_division=0,
            output_dict=True,
        )
    ).transpose()

    output.to_csv(
        OUTPUT_PREDICTIONS,
        index=False,
        encoding="utf-8-sig",
    )

    results_df.to_csv(
        OUTPUT_RULE_SEARCH,
        index=False,
        encoding="utf-8-sig",
    )

    cm.to_csv(
        OUTPUT_CONFUSION,
        encoding="utf-8-sig",
    )

    report_df.to_csv(
        OUTPUT_CLASSIFICATION_REPORT,
        encoding="utf-8-sig",
    )

    OUTPUT_METRICS.write_text(
        json.dumps(metrics, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n============================================================")
    print("WORLD CUP EVALUATION FINALIZADA")
    print("============================================================")
    print(f"Partidos evaluados: {metrics['matches_evaluated']}")
    print(f"Original Accuracy: {metrics['original_accuracy']:.4f}")
    print(f"Original F1 Macro: {metrics['original_f1_macro']:.4f}")
    print(f"Best Rule: {metrics['best_rule']}")
    print(f"Best Param: {metrics['best_param']}")
    print(f"Best Accuracy: {metrics['best_accuracy']:.4f}")
    print(f"Best F1 Macro: {metrics['best_f1_macro']:.4f}")

    print("\nClassification Report ajustado:")
    print(report_df)

    print("\nArchivos guardados:")
    print(OUTPUT_PREDICTIONS)
    print(OUTPUT_RULE_SEARCH)
    print(OUTPUT_CONFUSION)
    print(OUTPUT_CLASSIFICATION_REPORT)
    print(OUTPUT_METRICS)

    return output


if __name__ == "__main__":
    evaluate_worldcup()