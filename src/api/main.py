from typing import Optional

from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    BatchMatchPredictionRequest,
    BatchMatchPredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    CompetitionInfoResponse,
    MatchFeatures,
    MatchInfoResponse,
    MatchPredictionRequest,
    MatchPredictionResponse,
    ModelInfoResponse,
    PredictionResponse,
    TeamInfoResponse,
    TeamPredictionRequest,
)

from src.api.services import PredictionService


app = FastAPI(
    title="Football Match Prediction API",
    description=(
        "API para predicción online y batch de resultados "
        "de partidos de fútbol."
    ),
    version="1.0.0",
)


prediction_service = PredictionService()


# =========================================================
# GENERAL
# =========================================================

@app.get("/")
def root():

    return {
        "service": "Football Match Prediction API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.get(
    "/model",
    response_model=ModelInfoResponse,
)
def model_info():

    return prediction_service.model_info()


# =========================================================
# DISCOVERY
# =========================================================

@app.get(
    "/competitions",
    response_model=list[CompetitionInfoResponse],
)
def list_competitions():

    return prediction_service.list_competitions()


@app.get(
    "/teams",
    response_model=list[TeamInfoResponse],
)
def list_teams(
    competition: Optional[str] = None
):

    return prediction_service.list_teams(
        competition=competition
    )



@app.get(
    "/matches",
    response_model=list[MatchInfoResponse],
)
def list_matches(
    competition: Optional[str] = None
):

    return prediction_service.list_matches(
        competition=competition
    )


# =========================================================
# PREDICTIONS USING MATCH ID
# =========================================================

@app.post(
    "/predict_match",
    response_model=MatchPredictionResponse,
)
def predict_match(
    request: MatchPredictionRequest
):

    try:

        return prediction_service.predict_match(
            request.match_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


@app.post(
    "/predict_batch_matches",
    response_model=BatchMatchPredictionResponse,
)
def predict_batch_matches(
    request: BatchMatchPredictionRequest
):

    try:

        predictions = prediction_service.predict_batch_matches(
            request.match_ids
        )

        return {
            "predictions": predictions
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


# =========================================================
# PREDICTIONS USING TEAM NAMES
# =========================================================

@app.post(
    "/predict_by_teams",
    response_model=MatchPredictionResponse,
)
def predict_by_teams(
    request: TeamPredictionRequest
):

    try:

        return prediction_service.predict_by_teams(
            home_team=request.home_team,
            away_team=request.away_team,
            competition=request.competition,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


# =========================================================
# PREDICTIONS USING FEATURES
# =========================================================

@app.post(
    "/predict_features",
    response_model=PredictionResponse,
)
def predict_features(
    request: MatchFeatures
):

    try:

        result = prediction_service.predict_features(
            request.features
        )

        result["metadata"] = request.metadata

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


@app.post(
    "/predict_batch_features",
    response_model=BatchPredictionResponse,
)
def predict_batch_features(
    request: BatchPredictionRequest
):

    try:

        predictions = []

        for match in request.matches:

            result = prediction_service.predict_features(
                match.features
            )

            result["metadata"] = match.metadata

            predictions.append(result)

        return {
            "predictions": predictions
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e