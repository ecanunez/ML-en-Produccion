from typing import Any

from pydantic import BaseModel


# =========================================================
# REQUESTS
# =========================================================

class MatchFeatures(BaseModel):
    features: dict[str, float | int | None]
    metadata: dict[str, Any] | None = None


class BatchPredictionRequest(BaseModel):
    matches: list[MatchFeatures]


class MatchPredictionRequest(BaseModel):
    match_id: int


class BatchMatchPredictionRequest(BaseModel):
    match_ids: list[int]


class TeamPredictionRequest(BaseModel):
    competition: str | None = None
    home_team: str
    away_team: str


# =========================================================
# RESPONSES
# =========================================================

class PredictionResponse(BaseModel):
    prediction: str
    prob_away: float
    prob_draw: float
    prob_home: float
    metadata: dict[str, Any] | None = None


class MatchInfoResponse(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    competition: str | None = None
    continent: str | None = None
    season: int | str | None = None


class MatchPredictionResponse(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    competition: str | None = None
    prediction: str
    prob_away: float
    prob_draw: float
    prob_home: float


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class BatchMatchPredictionResponse(BaseModel):
    predictions: list[MatchPredictionResponse]


class ModelInfoResponse(BaseModel):
    version: str
    model_name: str
    feature_set: str
    n_features: int
    metrics: dict[str, Any]


class CompetitionInfoResponse(BaseModel):
    competition: str
    n_matches: int


class TeamInfoResponse(BaseModel):
    team: str