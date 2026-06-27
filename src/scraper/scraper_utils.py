from bs4 import BeautifulSoup
import re
from src.config.project_config import (
    BASE_URL
)
from src.config.competition_config import (
    COMPETITIONS,
    DOMESTIC_COMPETITIONS,
    INTERNATIONAL_COMPETITIONS,
)
from src.config.team_url_overrides import (
    TEAM_URL_OVERRIDES
)

def obtener_enlaces_competicion(url, page):

    page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    print("URL final:", page.url)
    print("Título:", page.title())

    page.wait_for_timeout(2000)

    soup = BeautifulSoup(
        page.content(),
        "html.parser"
    )

    enlaces = []

    for a in soup.select(
        "a[href*='/spielbericht/']"
    ):

        href = a.get("href")

        if not href:
            continue

        if href.startswith("/"):
            href = BASE_URL + href

        enlaces.append(href)

    enlaces = list(dict.fromkeys(enlaces))

    if enlaces:
        print("Primer enlace:", enlaces[0])

    return enlaces

def obtener_enlaces_partidos(url_calendario, page):

    try:

        page.goto(
            url_calendario,
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(2000)

        print(f"\nPágina cargada: {page.title()}")

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        enlaces = []

        # Buscar enlaces únicamente dentro de tablas
        tablas = soup.select("table")

        for tabla in tablas:

            links = tabla.select(
                "a[href*='/spielbericht/']"
            )

            for link in links:

                href = link.get("href")

                if not href:
                    continue

                if href.startswith("/"):

                    full_url = (
                        BASE_URL + href
                    )

                else:

                    full_url = href

                if (
                    "/index/spielbericht/"
                    not in full_url
                ):
                    full_url = full_url.replace(
                        "/spielbericht/",
                        "/index/spielbericht/"
                    )

                enlaces.append(full_url)

                enlaces_unicos = list(
                    dict.fromkeys(enlaces)
                )

                return enlaces_unicos

    except Exception as e:

        print(
            f"⚠️ Error en calendario: {e}"
        )

    return []

def extraer_datos_partido(url_partido, page, nombre_liga, anio_temporada, region_liga):

    try:

        if "/index/spielbericht/" not in url_partido:
            if "/spielbericht/" in url_partido:
                url_partido = url_partido.replace(
                    "/spielbericht/",
                    "/index/spielbericht/"
                )

        page.goto(
            url_partido,
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        # =====================================
        # EQUIPOS
        # =====================================

        equipo_l = "Desconocido"
        equipo_v = "Desconocido"

        try:

            selectores = [
                ".sb-team a.sb-club-link",
                ".sb-team a",
                ".matchheader a",
                ".data-header__club",
                "a[href*='/verein/']"
            ]

            for selector in selectores:

                elementos = page.locator(selector)

                if elementos.count() >= 2:

                    nombres = []

                    for i in range(elementos.count()):

                        try:

                            texto = (
                                elementos.nth(i)
                                .inner_text()
                                .strip()
                            )

                            if len(texto) > 2:
                                nombres.append(texto)

                        except Exception:
                            pass

                    nombres = list(dict.fromkeys(nombres))

                    if len(nombres) >= 2:

                        equipo_l = nombres[0]
                        equipo_v = nombres[1]
                        break

        except Exception as e:

            print(f"Error equipos: {e}")

        # =====================================
        # RESULTADO
        # =====================================

        resultado = "No jugado"

        try:

            resultado = (
                page.locator(
                    ".sb-endstand, .sb-result-number"
                )
                .first
                .inner_text()
                .strip()
            )

        except Exception:
            pass

        # =====================================
        # FECHA
        # =====================================
        fecha = None
        
        try:
            posibles_selectores = [
                ".sb-datum",
                ".sb-datum.hide-for-small",
                ".matchDate",
                "p.sb-datum",
                "div.sb-datum"
            ]

            for selector in posibles_selectores:

                elementos = page.locator(selector)

                if elementos.count() > 0:

                    texto = (
                        elementos.first
                        .inner_text()
                        .strip()
                    )

                    if texto:
                        fecha = texto
                        break

        except Exception as e:

            print(f"Error fecha: {e}")


        # =====================================
        # JUGADORES TITULARES
        # =====================================

        jugadores_local = []
        jugadores_visitante = []

        try:

            js_alineaciones = """
            () => {

                function extraerTitulares(bloque){

                    let jugadores = [];

                    if(!bloque){
                        return jugadores;
                    }

                    let links = bloque.querySelectorAll(
                        "a[href*='/profil/']"
                    );

                    for(let link of links){

                        let nombre = link.innerText.trim();

                        if(
                            nombre.length > 2 &&
                            !jugadores.includes(nombre)
                        ){
                            jugadores.push(nombre);
                        }

                        if(jugadores.length >= 11){
                            break;
                        }
                    }

                    return jugadores;
                }

                let resultado = {
                    local: [],
                    visitante: []
                };

                let bloques = document.querySelectorAll(
                    ".large-6.columns"
                );

                if(bloques.length >= 2){

                    resultado.local =
                        extraerTitulares(
                            bloques[0]
                        );

                    resultado.visitante =
                        extraerTitulares(
                            bloques[1]
                        );
                }

                return resultado;
            }
            """

            alineaciones = page.evaluate(
                js_alineaciones
            )

            jugadores_local = (
                alineaciones["local"]
                if "local" in alineaciones
                else []
            )

            jugadores_visitante = (
                alineaciones["visitante"]
                if "visitante" in alineaciones
                else []
            )

        except Exception as e:

            print(
                f"Error alineaciones: {e}"
            )

        # =====================================
        # DEBUG HTML
        # =====================================

        if (
            len(jugadores_local) == 0
            or
            len(jugadores_visitante) == 0
        ):

            with open(
                "debug_transfermarkt.html",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    page.content()
                )

            print(
                "⚠️ No se encontraron alineaciones."
            )

        # =====================================
        # REGISTRO
        # =====================================

        registro = {
            "region": region_liga,
            "liga": nombre_liga,
            "temporada": anio_temporada,
            "fecha": fecha,
            "equipo_local": equipo_l,
            "equipo_visitante": equipo_v,
            "resultado": resultado
        }

        for i in range(11):

            registro[
                f"local_jugador_{i+1}"
            ] = (
                jugadores_local[i]
                if i < len(jugadores_local)
                else "Desconocido"
            )

            registro[
                f"visitante_jugador_{i+1}"
            ] = (
                jugadores_visitante[i]
                if i < len(jugadores_visitante)
                else "Desconocido"
            )

        return registro

    except Exception as e:

        print(
            f"Error procesando partido: {e}"
        )

        return None
    
def construir_url_calendario(
    competition,
    temporada
):

    return (
        f"{BASE_URL}/"
        f"{competition['slug']}/"
        f"gesamtspielplan/"
        f"wettbewerb/"
        f"{competition['id_web']}/"
        f"saison_id/{temporada}"
    )

def construir_url_copa(
    competition,
    temporada
):

    return (
        f"{BASE_URL}/"
        f"{competition['slug']}/"
        f"gesamtspielplan/"
        f"pokalwettbewerb/"
        f"{competition['id_web']}/"
        f"saison_id/{temporada}"
    )

def obtener_partidos_futuros(
    url_fixture,
    page
):

    page.goto(
        url_fixture,
        wait_until="networkidle",
        timeout=60000
    )

    page.wait_for_timeout(3000)

    soup = BeautifulSoup(
        page.content(),
        "html.parser"
    )

    partidos = []

    for fila in soup.select("tr"):

        columnas = fila.find_all("td")

        if len(columnas) < 7:
            continue

        resultado = columnas[4].get_text(
            strip=True
        )

        # Solo partidos sin jugar
        if resultado != "-:-":
            continue

        local = columnas[2].get_text(
            " ",
            strip=True
        )

        visitante = columnas[6].get_text(
            " ",
            strip=True
        )

        link = columnas[4].find("a")

        href = (
            link.get("href")
            if link
            else None
        )

        partidos.append({
            "local": local,
            "visitante": visitante,
            "url": href
        })

    print(
        f"Partidos encontrados: "
        f"{len(partidos)}"
    )

    return partidos

def construir_url_fixture_liga(
    competition,
    season
):

    return (
        f"{BASE_URL}/"
        f"{competition['slug']}/"
        f"gesamtspielplan/"
        f"wettbewerb/"
        f"{competition['id_web']}"
        f"?saison_id={season}"
        f"&spieltagVon=1"
        f"&spieltagBis=38"
    )

def seleccionar_competiciones():

    print("\n=== TIPO DE COMPETICIONES ===\n")

    print("1 - Domésticas")
    print("2 - Internacionales")
    print("0 - Todas")

    opcion_tipo = input(
        "\nSelecciona una opción: "
    ).strip()

    if opcion_tipo == "0":

        return {
            "competiciones": COMPETITIONS,
            "tipo_competicion": "0",
            "continentes": []
        }

    if opcion_tipo == "1":

        competiciones_base = (
            DOMESTIC_COMPETITIONS
        )

    elif opcion_tipo == "2":

        competiciones_base = (
            INTERNATIONAL_COMPETITIONS
        )

    else:

        print(
            "\nOpción inválida."
        )

        return {}

    continentes_disponibles = [
        "Europe",
        "South America",
        "North America",
        "Asia",
        "Africa"
    ]

    print(
        "\n=== CONTINENTES DISPONIBLES ===\n"
    )

    for i, continente in enumerate(
        continentes_disponibles,
        start=1
    ):

        print(
            f"{i} - {continente}"
        )

    print("\n0 - Todos")

    opcion_continentes = input(
        "\nSelecciona uno o varios "
        "(ej: 1,2): "
    ).strip()

    if opcion_continentes == "0":

        return {
            "competiciones": competiciones_base,
            "tipo_competicion": opcion_tipo,
            "continentes": []
        }

    continentes_seleccionados = []

    for op in opcion_continentes.split(","):

        op = op.strip()

        if (
            op.isdigit()
            and 1 <= int(op) <= len(
                continentes_disponibles
            )
        ):

            continentes_seleccionados.append(
                continentes_disponibles[
                    int(op) - 1
                ]
            )

    competiciones = {}

    for clave, comp in (
        competiciones_base.items()
    ):

        if (
            comp["continent"]
            in continentes_seleccionados
        ):

            competiciones[
                clave
            ] = comp

    return {
        "competiciones": competiciones,
        "tipo_competicion": opcion_tipo,
        "continentes": continentes_seleccionados
    }

def buscar_url_equipo_transfermarkt(
    nombre_equipo,
    page
):

    if nombre_equipo in TEAM_URL_OVERRIDES:
        return TEAM_URL_OVERRIDES[nombre_equipo]
    
    search_url = (
        "https://www.transfermarkt.com/"
        "schnellsuche/ergebnis/schnellsuche"
        f"?query={nombre_equipo}"
    )

    page.goto(
        search_url,
        wait_until="networkidle",
        timeout=60000
    )

    soup = BeautifulSoup(
        page.content(),
        "html.parser"
    )

    links = soup.select(
        "table.items tbody tr td.hauptlink a"
    )

    for link in links:

        href = link.get("href", "")

        # Los clubes siempre contienen /verein/
        if "/verein/" not in href:
            continue

        return (
            "https://www.transfermarkt.com"
            + href
        )

    return None

def construir_url_plantilla(
    url_equipo,
    season
):
    match = re.search(
        r"/([^/]+)/startseite/verein/(\d+)",
        url_equipo
    )

    if not match:
        return None

    slug = match.group(1)
    team_id = match.group(2)

    return (
        f"https://www.transfermarkt.com/"
        f"{slug}/kader/"
        f"verein/{team_id}/"
        f"saison_id/{season}/plus/1"
    )

def extraer_plantilla_equipo(
    equipo,
    url_plantilla,
    page
):
    page.goto(
        url_plantilla,
        wait_until="networkidle"
    )

    soup = BeautifulSoup(
        page.content(),
        "html.parser"
    )

    jugadores = []

    filas = soup.select(
        "table.items tbody tr"
    )

    for fila in filas:

        try:

            link = fila.select_one(
                "td.hauptlink a"
            )

            if link is None:
                continue

            nombre = link.get_text(
                strip=True
            )

            href = link.get(
                "href",
                ""
            )

            match = re.search(
                r"/spieler/(\d+)",
                href
            )

            player_id = (
                int(match.group(1))
                if match
                else None
            )

            posicion = fila.select(
                "td"
            )[4].get_text(
                strip=True
            )

            edad = fila.select(
                "td"
            )[5].get_text(
                strip=True
            )

            valor = fila.select_one(
                "td.rechts.hauptlink"
            )

            valor = (
                valor.get_text(
                    strip=True
                )
                if valor
                else None
            )

            jugadores.append({
                "team": equipo,
                "player_id": player_id,
                "player": nombre,
                "position": posicion,
                "age": edad,
                "market_value": valor
            })

        except Exception:
            continue

    return jugadores