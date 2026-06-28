from pathlib import Path
from typing import Any

import pandas as pd
from joblib import load


ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    ROOT
    / "models"
    / "champion_model.pkl"
)

SCORING_DATASET_FILE = (
    ROOT
    / "data"
    / "processed"
    / "scoring_dataset.parquet"
)


class PredictionService:

    def __init__(self):

        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"No existe el modelo: {MODEL_FILE}"
            )

        if not SCORING_DATASET_FILE.exists():
            raise FileNotFoundError(
                f"No existe el scoring dataset: {SCORING_DATASET_FILE}"
            )

        self.artifact = load(
            MODEL_FILE
        )

        self.model = self.artifact["model"]
        self.features = self.artifact["features"]

        self.version = self.artifact.get("version", "unknown")
        self.model_name = self.artifact.get("model_name", "unknown")
        self.feature_set = self.artifact.get("feature_set", "unknown")
        self.metrics = self.artifact.get("metrics", {})

        self.scoring_df = pd.read_parquet(
            SCORING_DATASET_FILE
        ).reset_index(drop=True)

        self.scoring_df["match_id"] = self.scoring_df.index

    def model_info(self) -> dict[str, Any]:

        return {
            "version": self.version,
            "model_name": self.model_name,
            "feature_set": self.feature_set,
            "n_features": len(self.features),
            "metrics": self.metrics,
        }

    def list_competitions(self) -> list[dict[str, Any]]:

        if "competition" not in self.scoring_df.columns:
            return []

        competitions = (
            self.scoring_df
            .groupby("competition")
            .size()
            .reset_index(name="n_matches")
            .sort_values("competition")
        )

        return [
            {
                "competition": str(row["competition"]),
                "n_matches": int(row["n_matches"]),
            }
            for _, row in competitions.iterrows()
        ]

    def list_teams(
        self,
        competition: str | None = None
    ) -> list[dict[str, str]]:

        df = self.scoring_df.copy()

        if competition is not None:
            df = df[
                df["competition"] == competition
            ]

        teams = sorted(
            set(df["home_team"].dropna())
            | set(df["away_team"].dropna())
        )

        return [
            {
                "team": str(team)
            }
            for team in teams
        ]

    def list_matches(
        self,
        competition: str | None = None
    ) -> list[dict[str, Any]]:

        df = self.scoring_df.copy()

        if competition is not None:
            df = df[
                df["competition"] == competition
            ]

        cols = [
            "match_id",
            "home_team",
            "away_team",
            "competition",
            "continent",
            "season",
        ]

        available_cols = [
            col
            for col in cols
            if col in df.columns
        ]

        return (
            df[available_cols]
            .to_dict(orient="records")
        )

    def _get_match_row(
        self,
        match_id: int
    ) -> pd.DataFrame:

        if match_id < 0 or match_id >= len(self.scoring_df):
            raise ValueError(
                f"match_id inválido: {match_id}"
            )

        return self.scoring_df.iloc[[match_id]].copy()

    def _predict_frame(
        self,
        df: pd.DataFrame
    ) -> tuple[str, list[float]]:

        missing = [
            feature
            for feature in self.features
            if feature not in df.columns
        ]

        if missing:
            raise ValueError(
                "Faltan features requeridas: "
                + ", ".join(missing)
            )

        X = (
            df[self.features]
            .fillna(0)
        )

        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        return prediction, probabilities.tolist()

    def predict_match(
        self,
        match_id: int
    ) -> dict[str, Any]:

        row = self._get_match_row(
            match_id
        )

        prediction, probabilities = self._predict_frame(
            row
        )

        return {
            "match_id": match_id,
            "home_team": str(row["home_team"].iloc[0]),
            "away_team": str(row["away_team"].iloc[0]),
            "competition": (
                str(row["competition"].iloc[0])
                if "competition" in row.columns
                else None
            ),
            "prediction": str(prediction),
            "prob_away": float(probabilities[0]),
            "prob_draw": float(probabilities[1]),
            "prob_home": float(probabilities[2]),
        }

    def predict_batch_matches(
        self,
        match_ids: list[int]
    ) -> list[dict[str, Any]]:

        return [
            self.predict_match(match_id)
            for match_id in match_ids
        ]

    def predict_by_teams(
        self,
        home_team: str,
        away_team: str,
        competition: str | None = None,
    ) -> dict[str, Any]:

        df = self.scoring_df.copy()

        if competition is not None:
            df = df[
                df["competition"] == competition
            ]

        matches = df[
            (df["home_team"] == home_team)
            & (df["away_team"] == away_team)
        ]

        if matches.empty:
            raise ValueError(
                "No se encontró un partido con esos equipos."
            )

        if len(matches) > 1:
            raise ValueError(
                "Se encontró más de un partido. Especificar competición."
            )

        match_id = int(
            matches["match_id"].iloc[0]
        )

        return self.predict_match(
            match_id
        )

    def _build_input_frame(
        self,
        features: dict[str, float | int | None]
    ) -> pd.DataFrame:

        missing = [
            feature
            for feature in self.features
            if feature not in features
        ]

        if missing:
            raise ValueError(
                "Faltan features requeridas: "
                + ", ".join(missing)
            )

        row = {
            feature: features[feature]
            for feature in self.features
        }

        return pd.DataFrame(
            [row]
        ).fillna(0)

    def predict_features(
        self,
        features: dict[str, float | int | None]
    ) -> dict[str, Any]:

        X = self._build_input_frame(
            features
        )

        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        return {
            "prediction": str(prediction),
            "prob_away": float(probabilities[0]),
            "prob_draw": float(probabilities[1]),
            "prob_home": float(probabilities[2]),
        }