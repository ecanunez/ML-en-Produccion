from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.api.services import PredictionService


router = APIRouter(
    tags=["Demo"]
)

prediction_service = PredictionService()


@router.get("/demo", response_class=HTMLResponse)
def demo_page():

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <title>Football Prediction Demo</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 40px;
            }

            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 32px;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            }

            h1 {
                margin-top: 0;
                color: #1f2937;
            }

            label {
                display: block;
                margin-top: 20px;
                font-weight: bold;
                color: #374151;
            }

            select, button {
                width: 100%;
                padding: 12px;
                margin-top: 8px;
                border-radius: 8px;
                border: 1px solid #d1d5db;
                font-size: 16px;
            }

            button {
                margin-top: 28px;
                background: #2563eb;
                color: white;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }

            button:disabled {
                background: #9ca3af;
                cursor: not-allowed;
            }

            .result {
                margin-top: 32px;
                padding: 24px;
                border-radius: 12px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                display: none;
            }

            .prediction {
                font-size: 28px;
                font-weight: bold;
                color: #111827;
            }

            .probability-row {
                margin-top: 16px;
            }

            .bar-container {
                height: 18px;
                background: #e5e7eb;
                border-radius: 999px;
                overflow: hidden;
                margin-top: 6px;
            }

            .bar {
                height: 100%;
                background: #2563eb;
                width: 0%;
            }

            .error {
                margin-top: 24px;
                color: #b91c1c;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>⚽ Football Match Prediction</h1>
            <p>Seleccioná una competición, una fecha y un partido disponible.</p>

            <label for="competition">Competición</label>
            <select id="competition">
                <option value="">Cargando competiciones...</option>
            </select>

            <label for="date">Fecha</label>
            <select id="date" disabled>
                <option value="">Seleccioná una competición</option>
            </select>

            <label for="match">Partido</label>
            <select id="match" disabled>
                <option value="">Seleccioná una fecha</option>
            </select>

            <button id="predictButton" disabled onclick="predictMatch()">
                Predecir partido
            </button>

            <div id="error" class="error"></div>

            <div id="result" class="result">
                <h2 id="matchTitle"></h2>
                <div class="prediction" id="predictionText"></div>

                <div id="probabilities"></div>
            </div>
        </div>

        <script>
            const competitionSelect = document.getElementById("competition");
            const dateSelect = document.getElementById("date");
            const matchSelect = document.getElementById("match");
            const predictButton = document.getElementById("predictButton");
            const resultBox = document.getElementById("result");
            const errorBox = document.getElementById("error");

            async function fetchJson(url) {
                const response = await fetch(url);

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || "Error en la consulta");
                }

                return response.json();
            }

            async function loadCompetitions() {
                try {
                    const competitions = await fetchJson("/options/competitions");

                    competitionSelect.innerHTML = '<option value="">Seleccionar competición</option>';

                    competitions.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.name || item.competition || item;
                        option.textContent = item.name || item.competition || item;
                        competitionSelect.appendChild(option);
                    });

                } catch (error) {
                    showError(error.message);
                }
            }

            competitionSelect.addEventListener("change", async () => {
                resetSelect(dateSelect, "Cargando fechas...");
                resetSelect(matchSelect, "Seleccioná una fecha");
                matchSelect.disabled = true;
                predictButton.disabled = true;
                resultBox.style.display = "none";

                const competition = competitionSelect.value;

                if (!competition) {
                    dateSelect.disabled = true;
                    return;
                }

                try {
                    const dates = await fetchJson(
                        `/options/dates?competition=${encodeURIComponent(competition)}`
                    );

                    dateSelect.innerHTML = '<option value="">Seleccionar fecha</option>';

                    dates.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.date || item;
                        option.textContent = item.date || item;
                        dateSelect.appendChild(option);
                    });

                    dateSelect.disabled = false;

                } catch (error) {
                    showError(error.message);
                }
            });

            dateSelect.addEventListener("change", async () => {
                resetSelect(matchSelect, "Cargando partidos...");
                predictButton.disabled = true;
                resultBox.style.display = "none";

                const competition = competitionSelect.value;
                const date = dateSelect.value;

                if (!competition || !date) {
                    matchSelect.disabled = true;
                    return;
                }

                try {
                    const matches = await fetchJson(
                        `/options/matches?competition=${encodeURIComponent(competition)}&date=${encodeURIComponent(date)}`
                    );

                    matchSelect.innerHTML = '<option value="">Seleccionar partido</option>';

                    matches.forEach(match => {
                        const option = document.createElement("option");
                        option.value = match.match_id;
                        option.textContent = `${match.home_team} vs ${match.away_team}`;
                        matchSelect.appendChild(option);
                    });

                    matchSelect.disabled = false;

                } catch (error) {
                    showError(error.message);
                }
            });

            matchSelect.addEventListener("change", () => {
                predictButton.disabled = !matchSelect.value;
                resultBox.style.display = "none";
            });

            async function predictMatch() {
                const matchId = matchSelect.value;

                if (!matchId) {
                    return;
                }

                try {
                    clearError();

                    const result = await fetchJson(`/predict/match/${encodeURIComponent(matchId)}`);

                    renderResult(result);

                } catch (error) {
                    showError(error.message);
                }
            }

            function renderResult(result) {
                const prediction = result.prediction;
                const probabilities = result.probabilities || {
                    HOME: result.prob_home,
                    DRAW: result.prob_draw,
                    AWAY: result.prob_away,
                };

                const homeTeam = result.home_team || "Local";
                const awayTeam = result.away_team || "Visitante";

                document.getElementById("matchTitle").textContent =
                    `${homeTeam} vs ${awayTeam}`;

                document.getElementById("predictionText").textContent =
                    `Predicción: ${formatPrediction(prediction)}`;

                const probabilitiesBox = document.getElementById("probabilities");
                probabilitiesBox.innerHTML = "";

                Object.entries(probabilities).forEach(([label, value]) => {
                    const percent = Number(value * 100).toFixed(1);

                    const row = document.createElement("div");
                    row.className = "probability-row";

                    row.innerHTML = `
                        <strong>${formatPrediction(label)}:</strong> ${percent}%
                        <div class="bar-container">
                            <div class="bar" style="width: ${percent}%"></div>
                        </div>
                    `;

                    probabilitiesBox.appendChild(row);
                });

                resultBox.style.display = "block";
            }

            function formatPrediction(label) {
                const labels = {
                    HOME: "Gana local",
                    DRAW: "Empate",
                    AWAY: "Gana visitante"
                };

                return labels[label] || label;
            }

            function resetSelect(select, text) {
                select.innerHTML = `<option value="">${text}</option>`;
            }

            function showError(message) {
                errorBox.textContent = message;
            }

            function clearError() {
                errorBox.textContent = "";
            }

            loadCompetitions();
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


@router.get("/options/competitions")
def get_competition_options():

    return prediction_service.list_competitions()


@router.get("/options/dates")
def get_date_options(
    competition: str,
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


@router.get("/options/matches")
def get_match_options(
    competition: str,
    date: str,
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


@router.get("/predict/match/{match_id}")
def predict_match_by_path(
    match_id: str,
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