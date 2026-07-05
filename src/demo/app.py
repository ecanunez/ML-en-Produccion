from pathlib import Path
import sys
import unicodedata

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Football Match Predictor β",
    page_icon="⚽",
    layout="wide",
)


# =========================================================
# PATHS
# =========================================================

API_URL = "http://127.0.0.1:8000"

ROOT_DIR = Path(__file__).resolve().parents[2]

ASSETS_METADATA_PATH = (
    ROOT_DIR
    / "data"
    / "assets"
    / "team_assets.csv"
)

WORLDCUP_PREDICTIONS_PATH = (
    ROOT_DIR
    / "data"
    / "prediction_worldcup"
    / "predictions"
    / "worldcup_predictions.csv"
)

STYLES_PATH = (
    ROOT_DIR
    / "src"
    / "demo"
    / "styles.css"
)

DOCS_SCRIPTS_DIR = ROOT_DIR / "docs" / "scripts"

if str(DOCS_SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(DOCS_SCRIPTS_DIR))

from icons import ICONS
from style import PRIMARY, PRIMARY_LIGHT, TEXT, GRID


# =========================================================
# STYLE
# =========================================================

def load_css():
    css = STYLES_PATH.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"""
        <style>
        :root {{
            --primary: {PRIMARY};
            --primary-light: {PRIMARY_LIGHT};
            --text: {TEXT};
            --grid: {GRID};
        }}

        {css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_icon_html(
    icon_name,
    size=24,
    color=PRIMARY,
):
    if icon_name not in ICONS:
        return ""

    base_size = 256 if icon_name == "ball" else 24

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{size}"
         height="{size}"
         viewBox="0 0 {base_size} {base_size}"
         fill="none"
         stroke="{color}"
         stroke-width="2"
         stroke-linecap="round"
         stroke-linejoin="round">
    """

    for item in ICONS[icon_name]:
        kind = item[0]

        if kind == "path":
            svg += f'<path d="{item[1]}"/>'

        elif kind == "filled_path":
            svg += (
                f'<path d="{item[1]}" '
                f'fill="{color}" stroke="none"/>'
            )

        elif kind == "circle":
            cx, cy, r = item[1]
            svg += f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'

        elif kind == "rect":
            x, y, w, h, r = item[1]
            svg += (
                f'<rect x="{x}" y="{y}" '
                f'width="{w}" height="{h}" '
                f'rx="{r}" ry="{r}"/>'
            )

    svg += "</svg>"

    return svg


load_css()


# =========================================================
# DATA LOADERS
# =========================================================

def normalize_team_name(name):
    if name is None:
        return ""

    text = str(name).strip().lower()

    text = unicodedata.normalize(
        "NFKD",
        text,
    )

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    return text


@st.cache_data
def load_worldcup_predictions():
    if not WORLDCUP_PREDICTIONS_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(
        WORLDCUP_PREDICTIONS_PATH
    )


@st.cache_data
def load_team_assets():
    if not ASSETS_METADATA_PATH.exists():
        return {}

    assets_df = pd.read_csv(
        ASSETS_METADATA_PATH
    )

    assets = {}

    for _, row in assets_df.iterrows():
        logo_url = row.get("logo_url")

        if pd.isna(logo_url) or not logo_url:
            logo_url = row.get("source_url")

        if pd.isna(logo_url) or not logo_url:
            continue

        assets[
            normalize_team_name(row["team_name"])
        ] = logo_url

    return assets


TEAM_ASSETS = load_team_assets()


def get_team_logo(team_name):
    return TEAM_ASSETS.get(
        normalize_team_name(team_name)
    )


# =========================================================
# API
# =========================================================

def get_json(endpoint, params=None):
    response = requests.get(
        f"{API_URL}{endpoint}",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def predict_match(match_id):
    response = requests.post(
        f"{API_URL}/predict_match",
        json={"match_id": match_id},
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# MATCH HELPERS
# =========================================================

def get_match_period(match):
    return (
        match.get("date")
        or match.get("fecha")
        or match.get("fecha_partido")
        or match.get("match_date")
        or match.get("season")
        or match.get("temporada")
    )


def get_home_team(match):
    return (
        match.get("home_team")
        or match.get("equipo_local")
    )


def get_away_team(match):
    return (
        match.get("away_team")
        or match.get("equipo_visitante")
    )


def prediction_text(prediction, selected_match):
    if prediction == "HOME":
        return f"Gana {get_home_team(selected_match)}"

    if prediction == "AWAY":
        return f"Gana {get_away_team(selected_match)}"

    return "Empate"


def load_match_selector(matches):
    if not matches:
        st.warning(
            "No hay partidos disponibles para esta selección."
        )
        return None

    periods = sorted(
        {
            get_match_period(match)
            for match in matches
            if get_match_period(match) is not None
        }
    )

    if not periods:
        st.warning(
            "No hay temporadas/fechas disponibles."
        )
        st.json(matches[0])
        return None

    period = st.selectbox(
        "Temporada / Fecha",
        periods,
    )

    period_matches = [
        match
        for match in matches
        if get_match_period(match) == period
    ]

    match_labels = {
        f"{get_home_team(match)} vs {get_away_team(match)}": match
        for match in period_matches
    }

    selected_label = st.selectbox(
        "Partido",
        list(match_labels.keys()),
    )

    if selected_label is None:
        return None

    return match_labels[selected_label]


# =========================================================
# RENDER
# =========================================================

def render_team(team_name):
    logo_url = get_team_logo(team_name)

    if logo_url:
        st.image(
            logo_url,
            width=90,
        )
    else:
        st.markdown(
            f"""
            <div style="text-align:center;">
                {render_icon_html("ball", 46)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"<div class='team-name'>{team_name}</div>",
        unsafe_allow_html=True,
    )


def render_prediction(result, selected_match):
    home_team = get_home_team(selected_match)
    away_team = get_away_team(selected_match)

    pred_text = prediction_text(
        result["prediction"],
        selected_match,
    )

    st.divider()

    col1, col2, col3 = st.columns([4, 1, 4])

    with col1:
        render_team(home_team)

    with col2:
        st.markdown(
            "<div class='vs'>VS</div>",
            unsafe_allow_html=True,
        )

    with col3:
        render_team(away_team)

    st.markdown(
        f"""
        <div class="prediction-box">
            <div class="prediction-title">Predicción del modelo</div>
            <div class="prediction-value">
                {render_icon_html("champion", 28)} {pred_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    probabilities = {
        home_team: result["prob_home"],
        "Empate": result["prob_draw"],
        away_team: result["prob_away"],
    }

    st.markdown(
        f"""
        <div class="section-title">
            {render_icon_html("prediction", 24)}
            <h2>Probabilidades</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    for col, (label, prob) in zip(cols, probabilities.items()):
        col.metric(
            label=label,
            value=f"{prob * 100:.1f}%",
        )

    for label, prob in probabilities.items():
        st.write(f"**{label}**")
        st.progress(float(prob))
        st.caption(f"{prob * 100:.1f}%")



# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="icon-title">
        {render_icon_html("ball", 36)}
        <h1 class="main-title">Football Match Predictor</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="subtitle">
        Version β · Interactive Prediction Dashboard
    </p>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        f"""
        <div class="section-title">
            {render_icon_html("model", 24)}
            <h2>Panel técnico</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Seleccioná el módulo",
        [
            "Ligas Nacionales",
            "Mundial 2026",
        ],
    )

    st.divider()

    st.markdown("**Prediction Engine**")
    st.caption("Stacking Ensemble v1.0")

    st.markdown("**Features**")
    st.caption("30")

    st.markdown("**Target**")
    st.caption("HOME · DRAW · AWAY")


# =========================================================
# LIGAS NACIONALES
# =========================================================

if mode == "Ligas Nacionales":
    st.markdown(
        f"""
        <div class="section-title">
            {render_icon_html("team", 26)}
            <h2>Ligas Nacionales</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Predicciones para ligas nacionales."
    )

    competitions = get_json("/competitions")

    competition_names = [
        item["competition"] if "competition" in item else item["name"]
        for item in competitions
    ]

    competition = st.selectbox(
        "Competición",
        competition_names,
    )

    matches = get_json(
        "/matches",
        params={"competition": competition},
    )

    selected_match = load_match_selector(
        matches
    )

    if selected_match is not None:
        if st.button(
            "Predecir partido",
            use_container_width=True,
        ):
            result = predict_match(
                selected_match["match_id"]
            )

            render_prediction(
                result,
                selected_match,
            )


# =========================================================
# MUNDIAL 2026
# =========================================================

if mode == "Mundial 2026":
    st.markdown(
        f"""
        <div class="section-title">
            {render_icon_html("ball", 26)}
            <h2>Mundial 2026</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Predicciones generadas por el pipeline específico del Mundial."
    )

    wc_df = load_worldcup_predictions()

    if wc_df.empty:
        st.warning(
            "No se encontró worldcup_predictions.csv."
        )

    else:
        stages = sorted(
            wc_df["stage"]
            .dropna()
            .unique()
        )

        stage = st.selectbox(
            "Fase",
            stages,
        )

        stage_df = wc_df[
            wc_df["stage"] == stage
        ]

        match_labels = {
            f"{row.home_team} vs {row.away_team}": idx
            for idx, row in stage_df.iterrows()
        }

        selected_label = st.selectbox(
            "Partido",
            list(match_labels.keys()),
        )

        selected = stage_df.loc[
            match_labels[selected_label]
        ]

        result = {
            "prediction": selected["prediction"],
            "prob_home": selected["prob_home"],
            "prob_draw": selected["prob_draw"],
            "prob_away": selected["prob_away"],
        }

        selected_match = {
            "home_team": selected["home_team"],
            "away_team": selected["away_team"],
        }

        if st.button(
            "Mostrar predicción",
            use_container_width=True,
            key="worldcup_prediction",
        ):
            render_prediction(
                result,
                selected_match,
            )