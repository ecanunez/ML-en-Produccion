from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from joblib import load

from style import FONT, GRID, PRIMARY, PRIMARY_LIGHT, TEXT


ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "docs" / "assets" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRAINING_DATASET = ROOT / "data" / "processed" / "training_dataset.parquet"
BENCHMARK_RESULTS = ROOT / "src" / "reports" / "benchmark_results.csv"
CHAMPION_MODEL = ROOT / "models" / "champion_model.pkl"


NUMERIC_COLUMNS = {
    "Accuracy",
    "F1 Macro",
    "Precision Macro",
    "Recall Macro",
}


def format_float(value, decimals=4):
    return f"{float(value):.{decimals}f}".replace(".", ",")


def save_table(
    data: list[list[str]],
    columns: list[str],
    filename: str,
    title: str,
    numeric_columns: set[str] | None = None,
):
    numeric_columns = numeric_columns or NUMERIC_COLUMNS

    df = pd.DataFrame(
        data,
        columns=columns,
    )

    fig_height = 0.75 + 0.38 * len(df)

    fig, ax = plt.subplots(
        figsize=(9, fig_height)
    )

    ax.axis("off")

    ax.text(
        0,
        0.98,
        title,
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color=PRIMARY,
        fontname=FONT,
        ha="left",
        va="top",
    )

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="left",
        colLoc="left",
        bbox=[0, 0.02, 1, 0.82],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)

    for (row, col), cell in table.get_celld().items():

        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.6)

        if row == 0:
            cell.set_facecolor(PRIMARY)
            cell.set_text_props(
                color="white",
                weight="bold",
                fontname=FONT,
            )
            cell.get_text().set_ha("left")

        else:
            cell.set_facecolor(
                PRIMARY_LIGHT if row % 2 == 0 else "white"
            )

            cell.set_text_props(
                color=TEXT,
                fontname=FONT,
            )

            column_name = df.columns[col]

            if column_name in numeric_columns:
                cell.get_text().set_ha("right")
            else:
                cell.get_text().set_ha("left")

    output_path = OUTPUT_DIR / filename

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        transparent=False,
    )

    plt.close(fig)

    print(f"Tabla guardada en: {output_path}")


def generate_dataset_summary_table():
    df = pd.read_parquet(TRAINING_DATASET)

    n_rows = len(df)

    target_counts = (
        df["target"]
        .value_counts(normalize=True)
        .sort_index()
    )

    data = [
        ["Partidos históricos finales", f"{n_rows:,}".replace(",", ".")],
        ["Clases del target", "HOME / DRAW / AWAY"],
    ]

    for target_class in ["HOME", "DRAW", "AWAY"]:
        if target_class in target_counts:
            value = target_counts[target_class] * 100
            data.append(
                [
                    target_class,
                    f"{value:.1f}%".replace(".", ","),
                ]
            )

    if {
        "home_players_found",
        "away_players_found",
    }.issubset(df.columns):

        player_mapping_mean = (
            df[["home_players_found", "away_players_found"]]
            .mean()
            .mean()
        )

        data.append(
            [
                "Player mapping promedio",
                f"{player_mapping_mean:.1f} jugadores por equipo".replace(".", ","),
            ]
        )

    save_table(
        data=data,
        columns=["Indicador", "Resultado"],
        filename="table_01_dataset_summary.png",
        title="Tabla 1. Resumen de validación del dataset",
        numeric_columns=set(),
    )


def generate_model_benchmark_table():
    df = pd.read_csv(BENCHMARK_RESULTS)

    required_columns = {
        "model",
        "accuracy",
        "f1_macro",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            "Faltan columnas en benchmark_results.csv: "
            + ", ".join(missing)
        )

    df = df.sort_values(
        "f1_macro",
        ascending=False,
    )

    data = []

    for _, row in df.iterrows():
        data.append(
            [
                str(row["model"]),
                format_float(row["accuracy"]),
                format_float(row["f1_macro"]),
            ]
        )

    save_table(
        data=data,
        columns=["Modelo", "Accuracy", "F1 Macro"],
        filename="table_02_model_benchmark.png",
        title="Tabla 2. Benchmark de modelos evaluados",
    )


def generate_champion_model_table():
    artifact = load(CHAMPION_MODEL)

    metrics = artifact.get("metrics", {})

    data = [
        ["Modelo", str(artifact.get("model_name", "unknown"))],
        ["Versión", str(artifact.get("version", "unknown"))],
        ["Feature set", str(artifact.get("feature_set", "unknown"))],
        ["Cantidad de variables", str(len(artifact.get("features", [])))],
    ]

    metric_names = [
        ("accuracy", "Accuracy"),
        ("f1_macro", "F1 Macro"),
        ("precision_macro", "Precision Macro"),
        ("recall_macro", "Recall Macro"),
    ]

    for key, label in metric_names:
        if key in metrics:
            data.append(
                [
                    label,
                    format_float(metrics[key]),
                ]
            )

    save_table(
        data=data,
        columns=["Campo", "Valor"],
        filename="table_03_champion_model.png",
        title="Tabla 3. Ficha técnica del modelo campeón",
        numeric_columns=set(),
    )


def main():
    generate_dataset_summary_table()
    generate_model_benchmark_table()
    generate_champion_model_table()


if __name__ == "__main__":
    main()