import os
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.transfermarkt.es"

def extraer_datos_partido_internacional(
    url_partido,
    page,
    nombre_liga,
    anio_temporada,
    region_liga
):

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

                        except:
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

        except:
            pass

        # =====================================
        # DEBUG JUGADORES
        # =====================================

        try:

            total_perfiles = page.locator(
                "a[href*='/profil/']"
            ).count()

            print(
                f"Perfiles encontrados: "
                f"{total_perfiles}"
            )

        except:
            pass

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

            print(
                f"Local: {len(jugadores_local)} "
                f"Visitante: {len(jugadores_visitante)}"
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

            nombre_archivo = (
                url_partido.split("/")[-1]
                + ".html"
            )

            with open(
                nombre_archivo,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    page.content()
                )

            print(
                f"DEBUG guardado: "
                f"{nombre_archivo}"
            )

        # =====================================
        # REGISTRO
        # =====================================

        registro = {
            "region": region_liga,
            "liga": nombre_liga,
            "temporada": anio_temporada,
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

        print(
            f"{equipo_l} vs {equipo_v}"
        )
        return registro

    except Exception as e:

        print(
            f"Error procesando partido: {e}"
        )

        return None
    
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