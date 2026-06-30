from pathlib import Path
import pandas as pd
import svgwrite

from components import (
    add_arrow,
    add_box,
    add_caption,
    add_text,
    add_title,
)
from icons import draw_icon
from style import PRIMARY, PRIMARY_LIGHT, TEXT


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "docs" / "assets" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FEATURE_SELECTION_RESULTS = (
    ROOT
    / "src"
    / "reports"
    / "feature_selection_results.csv"
)


WIDTH = 900
HEIGHT = 1020

ARCH_WIDTH = 1200
ARCH_HEIGHT = 1200


def create_drawing(
    output_file: Path,
    width: int = WIDTH,
    height: int = HEIGHT,
):
    dwg = svgwrite.Drawing(
        str(output_file),
        size=(width, height),
        profile="full",
        debug=False,
    )

    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill="white",
        )
    )

    return dwg

def add_section_label(
    dwg,
    x,
    y,
    title,
    subtitle,
):
    line_w = 200

    dwg.add(
        dwg.line(
            start=(x - line_w / 2, y),
            end=(x + line_w / 2, y),
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    add_text(
        dwg,
        title,
        x,
        y + 34,
        size=20,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    dwg.add(
        dwg.line(
            start=(x - line_w / 2, y + 52),
            end=(x + line_w / 2, y + 52),
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    add_text(
        dwg,
        subtitle,
        x,
        y + 82,
        size=16,
        color=PRIMARY,
        anchor="middle",
    )

def generate_problem_representation():
    output_file = OUTPUT_DIR / "problem_representation.svg"

    dwg = create_drawing(output_file)

    add_title(
        dwg,
        title="REPRESENTACIÓN DEL PROBLEMA",
        subtitle="¿Cómo se convierte un partido de fútbol en una predicción?",
        width=WIDTH,
    )

    box_x = 120
    box_w = 660

    boxes = [
        {
            "title": "JUGADORES",
            "lines": [
                "22 futbolistas del encuentro",
                "atributos individuales",
            ],
            "icon": "player",
            "height": 100,
        },
        {
            "title": "EQUIPOS",
            "lines": [
                "representación agregada",
                "de los planteles",
            ],
            "icon": "team",
            "height": 100,
        },
        {
            "title": "PARTIDO",
            "lines": [
                "representación del encuentro",
                "30 variables",
            ],
            "icon": "match",
            "height": 120,
            "bullets": [
                "ELO",
                "valor de mercado",
                "forma reciente",
                "perfil del plantel",
            ],
        },
        {
            "title": "MODELO",
            "lines": [
                "modelo de Machine Learning",
                "entrenado sobre datos históricos",
            ],
            "icon": "model",
            "height": 100,
        },
        {
            "title": "PREDICCIÓN",
            "lines": [
                "probabilidades de resultado",
                "HOME · DRAW · AWAY",
            ],
            "icon": "prediction",
            "height": 100,
        },
    ]

    ys = [170, 315, 460, 635, 780]

    for box, y in zip(boxes, ys):
        add_box(
            dwg,
            box_x,
            y,
            box_w,
            box["height"],
            title=box["title"],
            lines=box["lines"],
            icon=box["icon"],
            bullets=box.get("bullets"),
        )

    for i in range(len(boxes) - 1):
        add_arrow(
            dwg,
            WIDTH / 2,
            ys[i] + boxes[i]["height"] + 8,
            ys[i + 1] - 16,
        )

    add_caption(
        dwg,
        width=WIDTH,
        number=1,
        y=940,
        text=(
            "Representación conceptual del flujo de información "
            "desde los jugadores hasta la predicción del modelo."
        ),
    )

    dwg.save()

    print(f"Figura guardada en: {output_file}")

def generate_historical_pipeline():
    output_file = OUTPUT_DIR / "historical_pipeline.svg"

    dwg = create_drawing(output_file)

    add_title(
        dwg,
        title="PROCESO DE ENTRENAMIENTO",
        subtitle="De los datos históricos al modelo campeón",
        width=WIDTH,
    )

    box_x = 120
    box_w = 660
    box_h = 100

    boxes = [
        {
            "title": "DATOS HISTÓRICOS",
            "lines": [
                "partidos ya disputados",
                "fuentes previamente validadas",
            ],
            "icon": "history",
        },
        {
            "title": "DATASET DE ENTRENAMIENTO",
            "lines": [
                "integración de fuentes",
                "target HOME · DRAW · AWAY",
            ],
            "icon": "road",
        },
        {
            "title": "INGENIERÍA DE VARIABLES",
            "lines": [
                "representación del partido",
                "fortaleza, jugadores y contexto",
            ],
            "icon": "tools",
        },
        {
            "title": "SELECCIÓN DE CARACTERÍSTICAS",
            "lines": [
                "reducción de complejidad",
                "conjunto final de variables",
            ],
            "icon": "filter",
        },
        {
            "title": "ENTRENAMIENTO Y EVALUACIÓN",
            "lines": [
                "comparación de modelos",
                "validación y métricas",
            ],
            "icon": "train",
        },
        {
            "title": "MODELO CAMPEÓN",
            "lines": [
                "artefacto versionado",
                "listo para inferencia",
            ],
            "icon": "champion",
        },
    ]

    ys = [160, 288, 416, 544, 672, 800]

    for box, y in zip(boxes, ys):
        add_box(
            dwg,
            box_x,
            y,
            box_w,
            box_h,
            title=box["title"],
            lines=box["lines"],
            icon=box["icon"],
        )

    for i in range(len(boxes) - 1):
        add_arrow(
            dwg,
            WIDTH / 2,
            ys[i] + box_h + 8,
            ys[i + 1] - 16,
        )

    add_caption(
        dwg,
        width=WIDTH,
        number=2,
        y=940,
        text=(
            "Secuencia conceptual del pipeline histórico utilizado "
            "para construir y exportar el modelo campeón."
        ),
    )

    dwg.save()

    print(f"Figura guardada en: {output_file}")

def add_architecture_box(
    dwg,
    x,
    y,
    w,
    h,
    title,
    lines,
    icon,
    stroke=PRIMARY,
    fill="white",
):
    dwg.add(
        dwg.rect(
            insert=(x, y),
            size=(w, h),
            rx=16,
            ry=16,
            fill=fill,
            stroke=stroke,
            stroke_width=2,
        )
    )

    dwg.add(
        dwg.rect(
            insert=(x + 20, y + 16),
            size=(76, h - 32),
            rx=13,
            ry=13,
            fill=PRIMARY_LIGHT,
            stroke="none",
        )
    )

    draw_icon(
        dwg,
        icon,
        x + 58,
        y + h / 2,
        size=42,
    )

    add_text(
        dwg,
        title,
        x + 120,
        y + 35,
        size=22,
        color=stroke,
        weight="bold",
    )

    for i, line in enumerate(lines):
        add_text(
            dwg,
            line,
            x + 120,
            y + 62 + i * 24,
            size=17,
            color=TEXT,
        )

def add_line_arrow(
    dwg,
    start,
    end,
    color=PRIMARY,
    width=3,
):
    x1, y1 = start
    x2, y2 = end

    dwg.add(
        dwg.line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=color,
            stroke_width=width,
            stroke_linecap="round",
        )
    )

    if y2 > y1:
        points = [
            (x2 - 10, y2 - 12),
            (x2 + 10, y2 - 12),
            (x2, y2 + 6),
        ]
    else:
        points = [
            (x2 - 10, y2 + 12),
            (x2 + 10, y2 + 12),
            (x2, y2 - 6),
        ]

    dwg.add(
        dwg.polygon(
            points=points,
            fill=color,
        )
    )

def add_split_arrow(
    dwg,
    x_center,
    y_start,
    y_branch,
    x_left,
    x_right,
):
    dwg.add(
        dwg.line(
            start=(x_center, y_start),
            end=(x_center, y_branch),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.line(
            start=(x_left, y_branch),
            end=(x_right, y_branch),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    add_line_arrow(
        dwg,
        (x_left, y_branch),
        (x_left, y_branch + 42),
    )

    add_line_arrow(
        dwg,
        (x_right, y_branch),
        (x_right, y_branch + 42),
    )

def add_merge_arrow(
    dwg,
    x_left,
    x_right,
    y_start,
    y_merge,
    x_center,
    y_end,
):
    dwg.add(
        dwg.line(
            start=(x_left, y_start),
            end=(x_left, y_merge),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.line(
            start=(x_right, y_start),
            end=(x_right, y_merge),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.line(
            start=(x_left, y_merge),
            end=(x_right, y_merge),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    add_line_arrow(
        dwg,
        (x_center, y_merge),
        (x_center, y_end),
    )

def generate_system_architecture():
    output_file = OUTPUT_DIR / "system_architecture.svg"

    dwg = create_drawing(
        output_file,
        width=ARCH_WIDTH,
        height=ARCH_HEIGHT,
    )

    add_title(
        dwg,
        title="ARQUITECTURA GENERAL DEL SISTEMA",
        subtitle="Entrenamiento e inferencia",
        width=ARCH_WIDTH,
    )

    box_w = 500
    box_h = 82
    x_center = ARCH_WIDTH / 2
    box_x = x_center - box_w / 2

    training_boxes = [
        {
            "title": "TRANSFERMARKT",
            "lines": ["scraping independiente"],
            "icon": "data",
            "y": 155,
        },
        {
            "title": "DATOS HISTÓRICOS",
            "lines": ["partidos y planteles históricos"],
            "icon": "history",
            "y": 260,
        },
        {
            "title": "PIPELINE HISTÓRICO",
            "lines": ["construcción del dataset base"],
            "icon": "road",
            "y": 365,
        },
        {
            "title": "DATASET + VARIABLES",
            "lines": ["representación del partido"],
            "icon": "tools",
            "y": 470,
        },
        {
            "title": "ENTRENAMIENTO",
            "lines": ["comparación y validación de modelos"],
            "icon": "train",
            "y": 575,
        },
    ]

    for box in training_boxes:
        add_architecture_box(
            dwg,
            box_x,
            box["y"],
            box_w,
            box_h,
            title=box["title"],
            lines=box["lines"],
            icon=box["icon"],
        )

    for i in range(len(training_boxes) - 1):
        add_line_arrow(
            dwg,
            (x_center, training_boxes[i]["y"] + box_h + 6),
            (x_center, training_boxes[i + 1]["y"] - 10),
        )

    champion_y = 690
    champion_w = 500
    champion_h = 90
    champion_x = x_center - champion_w / 2

    add_line_arrow(
        dwg,
        (x_center, training_boxes[-1]["y"] + box_h + 6),
        (x_center, champion_y - 10),
    )

    add_architecture_box(
        dwg,
        champion_x,
        champion_y,
        champion_w,
        champion_h,
        title="CHAMPION MODEL",
        lines=["modelo campeón versionado"],
        icon="champion",
        stroke="#B8860B",
        fill="#FFF8E6",
    )

    separator_y = 795

    dwg.add(
        dwg.line(
            start=(120, separator_y),
            end=(ARCH_WIDTH - 120, separator_y),
            stroke="#BFC7CE",
            stroke_width=3,
            stroke_dasharray="8,8",
        )
    )

    section_x = ARCH_WIDTH - 145

    add_section_label(
        dwg,
        x=section_x,
        y=330,
        title="ENTRENAMIENTO",
        subtitle="offline",
    )

    add_section_label(
        dwg,
        x=section_x,
        y=1025,
        title="INFERENCIA",
        subtitle="online / batch",
    )

    branch_y = 830

    left_x = 360
    right_x = 840

    add_split_arrow(
        dwg,
        x_center,
        champion_y + champion_h,
        branch_y,
        left_x,
        right_x,
    )

    inference_y = 880
    small_w = 440
    small_h = 100

    add_architecture_box(
        dwg,
        left_x - small_w / 2,
        inference_y,
        small_w,
        small_h,
        title="PIPELINE DE INFERENCIA",
        lines=[
            "Construcción del scoring dataset",
            "Predicción por lotes",
        ],
        icon="road",
    )

    add_architecture_box(
        dwg,
        right_x - small_w / 2,
        inference_y,
        small_w,
        small_h,
        title="API REST",
        lines=[
            "Predicción online",
            "Endpoint REST",
        ],
        icon="api",
    )

    prediction_y = 1010
    prediction_w = champion_w
    prediction_h = champion_h
    prediction_x = x_center - prediction_w / 2

    merge_y = 990

    add_merge_arrow(
        dwg,
        left_x,
        right_x,
        inference_y + small_h,
        merge_y,
        x_center,
        prediction_y - 12,
    )

    add_architecture_box(
        dwg,
        prediction_x,
        prediction_y,
        prediction_w,
        prediction_h,
        title="PREDICCIONES",
        lines=[
            "probabilidades de resultado",
            "HOME · DRAW · AWAY",
        ],
        icon="prediction",
    )

    add_caption(
        dwg,
        width=ARCH_WIDTH,
        number=3,
        y=1135,
        text=(
            "Arquitectura general del sistema: desde la recolección "
            "de datos históricos hasta la generación de predicciones."
        ),
    )

    dwg.save()

    print(f"Figura guardada en: {output_file}")

def load_feature_selection_points():
    df = pd.read_csv(FEATURE_SELECTION_RESULTS)
    df.columns = [c.lower().strip() for c in df.columns]

    points = []

    for _, row in df.iterrows():
        points.append(
            {
                "label": str(row["experiment"]),
                "n": int(row["n_features"]),
                "f1": float(row["f1_macro"]),
            }
        )

    points = sorted(points, key=lambda p: p["n"])

    return points

def generate_feature_selection():
    output_file = OUTPUT_DIR / "feature_selection.svg"

    width = 1250
    height = 1020

    dwg = create_drawing(
        output_file,
        width=width,
        height=height,
    )

    add_title(
        dwg,
        title="SELECCIÓN DE CARACTERÍSTICAS",
        subtitle="Búsqueda del conjunto óptimo de variables",
        width=width,
    )

    points = load_feature_selection_points()
    champion = max(points, key=lambda p: p["f1"])

    chart_x = 120
    chart_y = 200
    chart_w = 730
    chart_h = 390

    x_min = min(p["n"] for p in points)
    x_max = max(p["n"] for p in points)

    f1_min = min(p["f1"] for p in points)
    f1_max = max(p["f1"] for p in points)

    y_min = f1_min - 0.003
    y_max = f1_max + 0.003

    def x_scale(n):
        return chart_x + ((n - x_min) / (x_max - x_min)) * chart_w

    def y_scale(value):
        return chart_y + chart_h - ((value - y_min) / (y_max - y_min)) * chart_h

    y_ticks = [
        y_min,
        y_min + (y_max - y_min) * 0.25,
        y_min + (y_max - y_min) * 0.50,
        y_min + (y_max - y_min) * 0.75,
        y_max,
    ]

    for tick in y_ticks:
        y = y_scale(tick)

        dwg.add(
            dwg.line(
                start=(chart_x, y),
                end=(chart_x + chart_w, y),
                stroke="#D6DEE6",
                stroke_width=1.5,
                stroke_dasharray="6,6",
            )
        )

        add_text(
            dwg,
            f"{tick:.3f}",
            chart_x - 22,
            y + 6,
            size=17,
            color=TEXT,
            anchor="end",
        )

    dwg.add(
        dwg.line(
            start=(chart_x, chart_y + chart_h),
            end=(chart_x + chart_w + 35, chart_y + chart_h),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.line(
            start=(chart_x, chart_y + chart_h),
            end=(chart_x, chart_y - 25),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.polygon(
            points=[
                (chart_x + chart_w + 35, chart_y + chart_h),
                (chart_x + chart_w + 15, chart_y + chart_h - 10),
                (chart_x + chart_w + 15, chart_y + chart_h + 10),
            ],
            fill=PRIMARY,
        )
    )

    dwg.add(
        dwg.polygon(
            points=[
                (chart_x, chart_y - 25),
                (chart_x - 10, chart_y - 5),
                (chart_x + 10, chart_y - 5),
            ],
            fill=PRIMARY,
        )
    )

    add_text(
        dwg,
        "F1 Macro",
        chart_x - 45,
        chart_y - 42,
        size=19,
        color=PRIMARY,
        weight="bold",
    )

    add_text(
        dwg,
        "Número de variables",
        chart_x + chart_w / 2,
        chart_y + chart_h + 72,
        size=19,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    coords = [
        (
            x_scale(p["n"]),
            y_scale(p["f1"]),
        )
        for p in points
    ]

    for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
        dwg.add(
            dwg.line(
                start=(x1, y1),
                end=(x2, y2),
                stroke=PRIMARY,
                stroke_width=2.5,
                stroke_dasharray="7,4",
            )
        )

    for p in points:
        x = x_scale(p["n"])
        y = y_scale(p["f1"])

        dwg.add(
            dwg.line(
                start=(x, y),
                end=(x, chart_y + chart_h),
                stroke="#BFC7CE",
                stroke_width=1.5,
                stroke_dasharray="6,6",
            )
        )

        draw_icon(
            dwg,
            "ball",
            x,
            y,
            size=34,
        )

        label_y = y - 28
        if p["n"] == champion["n"]:
            label_y = y - 88

        add_text(
            dwg,
            f"{p['f1']:.4f}",
            x,
            label_y,
            size=16,
            color=PRIMARY,
            weight="bold",
            anchor="middle",
        )

        add_text(
            dwg,
            str(p["n"]),
            x,
            chart_y + chart_h + 28,
            size=17,
            color=TEXT,
            weight="bold",
            anchor="middle",
        )

        add_text(
            dwg,
            f"({p['label']})",
            x,
            chart_y + chart_h + 52,
            size=15,
            color=TEXT,
            anchor="middle",
        )

    cx = x_scale(champion["n"])
    cy = y_scale(champion["f1"])

    draw_icon(
        dwg,
        "star",
        cx,
        cy - 58,
        size=42,
    )

    add_text(
        dwg,
        "MODELO CAMPEÓN",
        cx + 34,
        cy - 56,
        size=17,
        color="#B8860B",
        weight="bold",
    )

    decision_x = 900
    decision_y = 265
    decision_w = 290
    decision_h = 335

    dwg.add(
        dwg.rect(
            insert=(decision_x, decision_y),
            size=(decision_w, decision_h),
            rx=18,
            ry=18,
            fill="white",
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    add_text(
        dwg,
        "DECISIÓN FINAL",
        decision_x + decision_w / 2,
        decision_y + 45,
        size=20,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    dwg.add(
        dwg.line(
            start=(decision_x + 45, decision_y + 65),
            end=(decision_x + decision_w - 45, decision_y + 65),
            stroke=PRIMARY,
            stroke_width=4,
            stroke_linecap="round",
        )
    )

    bullets = [
        "Mejor rendimiento",
        "Menor complejidad",
        "Menor tiempo",
        "Menor riesgo de sobreajuste",
    ]

    for i, bullet in enumerate(bullets):
        y = decision_y + 110 + i * 48

        dwg.add(
            dwg.circle(
                center=(decision_x + 35, y - 7),
                r=9,
                fill=PRIMARY,
            )
        )

        add_text(
            dwg,
            "✓",
            decision_x + 35,
            y - 2,
            size=13,
            color="white",
            weight="bold",
            anchor="middle",
        )

        add_text(
            dwg,
            bullet,
            decision_x + 55,
            y,
            size=15,
            color=TEXT,
        )

    table_x = 120
    table_y = 725
    table_w = 730
    cell_h = 34

    label_cell_w = 135
    value_cell_w = table_w / len(points)

    dwg.add(
        dwg.rect(
            insert=(table_x, table_y),
            size=(label_cell_w, cell_h * 2),
            fill=PRIMARY,
            stroke=PRIMARY,
            stroke_width=1.5,
        )
    )

    add_text(
        dwg,
        "Conjunto",
        table_x + label_cell_w / 2,
        table_y + 23,
        size=15,
        color="white",
        weight="bold",
        anchor="middle",
    )

    add_text(
        dwg,
        "Nº variables",
        table_x + label_cell_w / 2,
        table_y + 57,
        size=15,
        color="white",
        weight="bold",
        anchor="middle",
    )

    for i, p in enumerate(points):
        x = table_x + label_cell_w + value_cell_w * i

        for row, text in enumerate([p["label"], str(p["n"])]):
            dwg.add(
                dwg.rect(
                    insert=(x, table_y + row * cell_h),
                    size=(value_cell_w, cell_h),
                    fill="white",
                    stroke="#BFC7CE",
                    stroke_width=1.2,
                )
            )

            add_text(
                dwg,
                text,
                x + value_cell_w / 2,
                table_y + row * cell_h + 23,
                size=15,
                color=TEXT,
                anchor="middle",
            )

    add_caption(
        dwg,
        width=width,
        number=4,
        y=900,
        text=(
            "Evolución del F1 Macro según la cantidad de variables. "
            "Top30 se selecciona por su equilibrio entre desempeño y complejidad."
        ),
    )

    dwg.save()

    print(f"Figura guardada en: {output_file}")


def main():
    generate_problem_representation()
    generate_historical_pipeline()
    generate_system_architecture()
    generate_feature_selection()


if __name__ == "__main__":
    main()