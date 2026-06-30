from pathlib import Path
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright


DOCS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCS_DIR.parent

REPORT_MD = DOCS_DIR / "final_report.md"
OUTPUT_DIR = DOCS_DIR / "output"
OUTPUT_PDF = OUTPUT_DIR / "Informe del Proyecto.pdf"

TEMP_MD = DOCS_DIR / "_report_build.md"
TEMP_HTML = DOCS_DIR / "_report_build.html"

TABLE_SCRIPT = DOCS_DIR / "scripts" / "generate_tables.py"
FIGURE_SCRIPT = DOCS_DIR / "scripts" / "generate_infographics_svg.py"
CSS_FILE = DOCS_DIR / "scripts" / "report.css"


def run(command, cwd=PROJECT_ROOT):
    print("Ejecutando:", " ".join(map(str, command)))
    subprocess.run(command, cwd=cwd, check=True)


def build_temp_markdown():
    text = REPORT_MD.read_text(encoding="utf-8")

    text = text.replace("..assets/", "assets/")
    text = text.replace("../assets/", "assets/")

    text = re.sub(
        r"^# .+\n+",
        "",
        text,
        count=1,
    )

    TEMP_MD.write_text(text, encoding="utf-8")


def build_html():
    command = [
        "pandoc",
        TEMP_MD.name,
        "-o",
        TEMP_HTML.name,
        "--standalone",
        "--toc",
        "--metadata",
        "title=Machine Learning en Producción",
        "--metadata",
        "subtitle=Predicción de resultados de partidos de fútbol mediante representación basada en jugadores",
        "--metadata",
        "author=Agustina Núñez",
        "--metadata",
        "date=2026",
        "--metadata",
        "repository=https://github.com/ecanunez/ML-en-Produccion",
    ]


    run(command, cwd=DOCS_DIR)

    html = TEMP_HTML.read_text(encoding="utf-8")
    css = CSS_FILE.read_text(encoding="utf-8")

    repository = """
    <div class="repository">
        <h3>Repositorio del proyecto</h3>
        <a href="https://github.com/ecanunez/ML-en-Produccion">
            https://github.com/ecanunez/ML-en-Produccion
        </a>
    </div>
    """

    html = html.replace(
        "</header>",
        repository + "\n</header>",
    )

    html = html.replace(
        "</head>",
        f"<style>\n{css}\n</style>\n</head>",
    )

    TEMP_HTML.write_text(html, encoding="utf-8")


def html_to_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(
            TEMP_HTML.resolve().as_uri(),
            wait_until="networkidle",
        )

        page.pdf(
            path=str(OUTPUT_PDF),
            format="A4",
            print_background=True,
            margin={
                "top": "18mm",
                "right": "18mm",
                "bottom": "18mm",
                "left": "18mm",
            },
        )

        browser.close()


def main():
    if not REPORT_MD.exists():
        raise FileNotFoundError(f"No se encontró el reporte: {REPORT_MD}")

    run([sys.executable, str(TABLE_SCRIPT)])
    run([sys.executable, str(FIGURE_SCRIPT)])

    build_temp_markdown()
    build_html()
    html_to_pdf()

    print(f"\nPDF generado en: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()