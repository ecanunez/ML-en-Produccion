import glob
from datetime import datetime
import os
import pandas as pd

from src.config.dataset_config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)

INPUT_DIR = (
    RAW_DATA_DIR
    / "team_squads"
)

OUTPUT_DIR = (
    PROCESSED_DATA_DIR
    / "team_features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def convertir_valor_mercado(valor):

    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    valor = valor.replace("€", "")

    try:

        if valor.endswith("bn"):
            return float(
                valor.replace("bn", "")
            ) * 1_000_000_000

        if valor.endswith("m"):
            return float(
                valor.replace("m", "")
            ) * 1_000_000

        if valor.endswith("k"):
            return float(
                valor.replace("k", "")
            ) * 1_000

        return float(valor)

    except Exception:

        return None

def convertir_edad(edad):

    if pd.isna(edad):
        return None

    edad = str(edad)

    if "(" not in edad:
        return None

    try:

        return int(
            edad.split("(")[1]
            .replace(")", "")
        )

    except Exception:

        return None

def clasificar_posicion(posicion):

    posicion = str(
        posicion
    ).lower()

    if (
        "centre-back" in posicion
        or "left-back" in posicion
        or "right-back" in posicion
        or "defender" in posicion
    ):
        return "DEF"

    if (
        "midfield" in posicion
    ):
        return "MID"

    if (
        "winger" in posicion
        or "forward" in posicion
        or "striker" in posicion
    ):
        return "ATT"

    return "OTHER"

def obtener_ultimo_team_squads():

    archivos = glob.glob(
        os.path.join(
            INPUT_DIR,
            "team_squads_*.csv"
        )
    )

    if not archivos:
        raise FileNotFoundError(
            "No se encontraron archivos team_squads"
        )

    return max(
        archivos,
        key=os.path.getmtime
    )


def main():

    archivo = obtener_ultimo_team_squads()

    print(
        f"\nLeyendo:\n{archivo}"
    )

    df = pd.read_csv(
        archivo
    )

    df["market_value_num"] = (
        df["market_value"]
        .apply(
            convertir_valor_mercado
        )
    )

    df["age_num"] = (
        df["age"]
        .apply(
            convertir_edad
        )
    )

    df["group"] = (
        df["position"]
        .apply(
            clasificar_posicion
        )
    )

    registros = []

    for team, g in df.groupby("team"):

        team_market_value = (
            g["market_value_num"]
            .sum()
        )

        avg_player_value = (
            g["market_value_num"]
            .mean()
        )

        avg_age = (
            g["age_num"]
            .mean()
        )

        def_value = (
            g.loc[
                g["group"] == "DEF",
                "market_value_num"
            ].sum()
        )

        mid_value = (
            g.loc[
                g["group"] == "MID",
                "market_value_num"
            ].sum()
        )

        att_value = (
            g.loc[
                g["group"] == "ATT",
                "market_value_num"
            ].sum()
        )

        registros.append({
            "team": team,
            "n_players": len(g),
            "team_market_value": team_market_value,
            "avg_player_value": avg_player_value,
            "avg_age": avg_age,
            "def_market_value": def_value,
            "mid_market_value": mid_value,
            "att_market_value": att_value
        })

    df_out = pd.DataFrame(
        registros
    )

    fecha = datetime.now().strftime(
        "%Y%m%d"
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        f"team_features_{fecha}.csv"
    )

    df_out.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nArchivo generado:\n{output_file}"
    )

    print(
        f"Equipos: {len(df_out)}"
    )


if __name__ == "__main__":
    main()
