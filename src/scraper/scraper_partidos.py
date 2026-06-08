import os
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# CONSTANTES Y CONFIGURACIÓN
DATA_RAW_DIR = os.path.join("data", "raw", "games")
SEASON_DIR = os.path.join(DATA_RAW_DIR, 'seasons')
os.makedirs(SEASON_DIR, exist_ok=True)

BASE_URL = "https://www.transfermarkt.es"
TEMPORADAS = [2022, 2023, 2024, 2025]

CONFIG_LIGAS = {
    "Europa": {
        "1": {"nombre": "LaLiga", "id_web": "ES1", "slug": "laliga"},
        "2": {"nombre": "Premier League", "id_web": "GB1", "slug": "premier-league"},
        "3": {"nombre": "Serie A", "id_web": "IT1", "slug": "serie-a"},
        "4": {"nombre": "Bundesliga", "id_web": "L1", "slug": "bundesliga"},
        "5": {"nombre": "Ligue 1", "id_web": "FR1", "slug": "ligue-1"},
        "6": {"nombre": "Primeira Liga", "id_web": "PO1", "slug": "liga-nos"},
        "7": {"nombre": "Eredivisie", "id_web": "NL1", "slug": "eredivisie"},
        "8": {"nombre": "Jupiler Pro League", "id_web": "BE1", "slug": "jupiler-pro-league"},
        "9": {"nombre": "Süper Lig", "id_web": "TR1", "slug": "super-lig"},
        "10": {"nombre": "Chance Liga", "id_web": "CZ1", "slug": "chance-liga"}
    },
    "Sudamérica": {
        "11": {"nombre": "Brasileirao", "id_web": "BRA1", "slug": "campeonato-brasileiro-serie-a"},
        "12": {"nombre": "Liga Profesional Argentina", "id_web": "AR1N", "slug": "liga-profesional-de-futbol"},
        "13": {"nombre": "Bolivia División Profesional", "id_web": "BODP", "slug": "division-profesional"},
        "14": {"nombre": "Chile Primera División", "id_web": "CLPD", "slug": "primera-division"},
        "15": {"nombre": "Colombia Primera A", "id_web": "COAA", "slug": "primera-a"},
        "16": {"nombre": "Ecuador LigaPro", "id_web": "ECP1", "slug": "ligapro"},
        "17": {"nombre": "Paraguay Primera División", "id_web": "PAR1", "slug": "primera-division"},
        "18": {"nombre": "Perú Liga 1", "id_web": "PEL1", "slug": "liga-1"},
        "19": {"nombre": "Uruguay Primera División", "id_web": "URU1", "slug": "primera-division"},
        "20": {"nombre": "Venezuela Primera División", "id_web": "VFP1", "slug": "primera-division"}
    },
    "Norteamérica": {
        "21": {"nombre": "Major League Soccer", "id_web": "MLS1", "slug": "major-league-soccer"},
        "22": {"nombre": "Liga MX Clausura", "id_web": "MEX1", "slug": "liga-mx-clausura"},
        "23": {"nombre": "Liga MX Apertura", "id_web": "MEX1", "slug": "liga-mx-apertura"}
    },
    "Asia": {
        "24": {"nombre": "Saudi Pro League", "id_web": "SA1", "slug": "saudi-pro-league"},
        "25": {"nombre": "J1 League", "id_web": "JAP1", "slug": "j1-league"},
        "26": {"nombre": "K-League 1", "id_web": "KOR1", "slug": "k-league-1"}
    },
    "África": {
        "27": {"nombre": "Egipto Premier League", "id_web": "EGY1", "slug": "egyptian-premier-league"},
        "28": {"nombre": "Botola Pro", "id_web": "MAR1", "slug": "botola-pro"},
        "29": {"nombre": "Túnez Ligue 1", "id_web": "TUN1", "slug": "ligue-1-professionnelle-1"},
        "30": {"nombre": "Linafoot", "id_web": "COD1", "slug": "linafoot"}
    }
}

def obtener_enlaces_partidos(url_calendario, page):
    try:
        page.goto(url_calendario, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        
        enlaces = []
        for a in soup.find_all("a", href=True):
            if "/spielbericht/" in a['href']:
                full_url = BASE_URL + a['href'] if a['href'].startswith("/") else a['href']
                enlaces.append(full_url)
        
        enlaces_unicos = list(set(enlaces))
        print(f"      ✅ Se encontraron {len(enlaces_unicos)} partidos.")
        return enlaces_unicos
    except Exception as e:
        print(f"    ⚠️ Error en calendario: {e}")
        return []

def extraer_datos_partido(url_partido, page, nombre_liga, anio_temporada, region_liga):
    try:
        # Espera agresiva de red para asegurar que el marcador cargue con JS
        page.goto(url_partido, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(random.randint(1500, 2500))
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        equipos = soup.find_all("nobr")
        if len(equipos) < 2:
            return None

        # Extracción segura del Marcador Real
        resultado = "No jugado"
        marcador_contenedor = soup.find("div", class_="sb-zeit-ergebnis")
        if marcador_contenedor:
            marcador_span = marcador_contenedor.find("span", class_="sb-endstand") or \
                            marcador_contenedor.find("div", class_="sb-result-number")
            if marcador_span:
                resultado = " ".join(marcador_span.text.split())
        
        # Plan de contingencia si la clase cambia
        if resultado == "No jugado":
            resultado_box = soup.find("div", class_="sb-team-results") or \
                            soup.find("div", class_="ergebnis-box")
            if resultado_box:
                resultado = " ".join(resultado_box.text.split())

        # Base del registro (Añadida la variable region aquí)
        registro = {
            "region": region_liga,
            "liga": nombre_liga,
            "temporada": anio_temporada,
            "equipo_local": equipos[0].text.strip(),
            "equipo_visitante": equipos[1].text.strip(),
            "resultado": resultado
        }

        # Extracción ULTRA-PRECISA de los 11 titulares en cancha
        # 'yw1' contiene la tabla del equipo local, 'yw2' la del visitante
        for idx, tabla_id in enumerate(["yw1", "yw2"]):
            key_pref = "local" if idx == 0 else "visitante"
            tabla_titulares = soup.find("div", id=tabla_id)
            
            if tabla_titulares:
                # Buscamos solo las celdas de jugadores principales en la alineación
                celdas_jugadores = tabla_titulares.find_all("td", class_="hauptlink")
                
                # Extraemos el texto de los nombres reales de los futbolistas
                jugadores = []
                for celda in celdas_jugadores:
                    link = celda.find("a")
                    if link and "/profil/" in link.get("href", "") and link.text.strip():
                        nombre_jugador = link.text.strip()
                        if nombre_jugador not in jugadores:
                            jugadores.append(nombre_jugador)
                
                # Asignamos estrictamente los primeros 11 (Alineación Inicial)
                for j, jug in enumerate(jugadores[:11]):
                    registro[f"{key_pref}_jugador_{j+1}"] = jug

        return registro
    except Exception as e:
        print(f"Error procesando {url_partido}: {e}")
        return None

if __name__ == "__main__":
    print("\n=== SELECCIÓN DE REGIÓN ===")
    regiones = list(CONFIG_LIGAS.keys())
    for i, region in enumerate(regiones, 1): 
        print(f" {i} - {region}")
    
    opcion_reg = input("\nSelecciona el número de región: ").strip()
    
    if opcion_reg.isdigit() and 1 <= int(opcion_reg) <= len(regiones):
        region_sel = regiones[int(opcion_reg) - 1]
        print(f"\n🚀 Iniciando extracción con Playwright para: {region_sel}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            for liga in CONFIG_LIGAS[region_sel].values():
                print(f"\n--- PROCESANDO LIGA: {liga['nombre']} ---")
                
                for anio in TEMPORADAS:
                    print(f" > Procesando {anio}...")
                    url = f"{BASE_URL}/{liga['slug']}/gesamtspielplan/wettbewerb/{liga['id_web']}/saison_id/{anio}"
                    
                    enlaces = obtener_enlaces_partidos(url, page)
                    
                    if enlaces:
                        datos_temporada = []
                        for link in enlaces:
                            # Pasamos region_sel como parámetro a la función
                            datos = extraer_datos_partido(link, page, liga['nombre'], anio, region_sel)
                            if datos:
                                datos_temporada.append(datos)
                        
                        if datos_temporada:
                            df_temp = pd.DataFrame(datos_temporada)
                            file_name = f"{liga['nombre'].lower().replace(' ', '_')}_{anio}.csv"
                            df_temp.to_csv(os.path.join(SEASON_DIR, file_name), index=False)
                            print(f"   ✅ Temporada {anio} guardada con Región y Alineación Oficial.")
            
            browser.close()
            print("\n🏁 Proceso de scraping completado. Navegador cerrado.")
    else:
        print("❌ Opción inválida.")