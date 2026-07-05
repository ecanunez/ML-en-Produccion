from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from src.api.services import PredictionService


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Football Prediction Demo",
    description="Demo web para consultar predicciones del modelo campeón.",
    version="2.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

prediction_service = PredictionService()


# =========================================================
# PAGES
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@app.get("/clubs", response_class=HTMLResponse)
def clubs(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="clubs.html",
        context={}
    )


@app.get("/worldcup", response_class=HTMLResponse)
def worldcup(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="worldcup.html",
        context={}
    )

# =========================================================
# OPTIONS - CLUBS
# =========================================================

@app.get("/api/clubs/competitions")
def get_club_competitions():

    competitions = prediction_service.list_competitions()

    return competitions


@app.get("/api/clubs/dates")
def get_club_dates(
    competition: str = Query(...)
):

    try:

        return prediction_service.list_dates(
            competition=competition
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


@app.get("/api/clubs/matches")
def get_club_matches(
    competition: str = Query(...),
    date: str = Query(...),
):

    try:

        return prediction_service.list_matches(
            competition=competition,
            date=date,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


# =========================================================
# OPTIONS - WORLD CUP
# =========================================================

@app.get("/api/worldcup/dates")
def get_worldcup_dates():

    try:

        return prediction_service.list_dates(
            competition="FIFA World Cup"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


@app.get("/api/worldcup/matches")
def get_worldcup_matches(
    date: str = Query(...)
):

    try:

        return prediction_service.list_matches(
            competition="FIFA World Cup",
            date=date,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


# =========================================================
# PREDICTION
# =========================================================

@app.get("/api/predict/match/{match_id}")
def predict_match(
    match_id: str
):

    try:

        return prediction_service.predict_match(
            match_id=match_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e