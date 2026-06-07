import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. CONSTANTES Y CONFIGURACIÓN (Toda la lista de CONFIG_LIGAS)
DATA_RAW_DIR = os.path.join("data", "raw", "games")
TOTALS_DIR = os.path.join(DATA_RAW_DIR, 'totals') # Definimos esto globalmente
os.makedirs(TOTALS_DIR, exist_ok=True)

BASE_URL = "https://www.transfermarkt.es"
HEADERS = {"User-Agent": "Mozilla/5.0"}
EMPORADAS = [2022, 2023, 2024, 2025]

# Estructura jerárquica de ligas
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


def obtener_enlaces_partidos(url_calendario):
    try:
        response = requests.get(url_calendario, headers=HEADERS, timeout=15)
        if response.status_code != 200: return []
        soup = BeautifulSoup(response.text, "html.parser")
        enlaces = [BASE_URL + link.get("href") for link in soup.find_all("a", class_="ergebnis-link") if "/spielbericht/" in link.get("href", "")]
        return list(dict.fromkeys(enlaces))
    except Exception: return []

def extraer_datos_partido(url_partido, nombre_liga, anio_temporada):
    try:
        response = requests.get(url_partido, headers=HEADERS, timeout=15)
        if response.status_code != 200: return None
        soup = BeautifulSoup(response.text, "html.parser")
        
        equipos = soup.find_all("nobr")
        if len(equipos) < 2: return None
        
        ergebnis_box = soup.find("div", class_="ergebnis-box")
        resultado = " ".join(ergebnis_box.text.split()) if ergebnis_box else "No jugado"
        
        registro = {
            "liga": nombre_liga,
            "temporada": anio_temporada,
            "equipo_local": equipos[0].text.strip(),
            "equipo_visitante": equipos[1].text.strip(),
            "resultado": resultado
        }
        
        # --- DEFINIMOS BLOQUES AQUÍ (Esto solucionará tu error) ---
        bloques = soup.find_all("div", class_="large-6 columns")
        
        for idx, i in enumerate([0, 1]):
            key_pref = "local" if idx == 0 else "visitante"
            if len(bloques) > i:
                # Búsqueda flexible: busca tabla con clase 'items', 'inline-table' o cualquier tabla
                tabla = bloques[i].find("table", class_="items") or \
                        bloques[i].find("table", class_="inline-table") or \
                        bloques[i].find("table")
                
                if tabla:
                    # Buscamos enlaces que llevan al perfil del jugador
                    jugadores = [a.text.strip() for a in tabla.find_all("a") if "/profil/" in a.get("href", "")]
                    for j, jug in enumerate(jugadores[:11]):
                        registro[f"{key_pref}_jugador_{j+1}"] = jug
        
        return registro
    except Exception as e:
        print(f"Error procesando {url_partido}: {e}")
        return None


if __name__ == "__main__":
    print("\n=== SELECCIÓN DE REGIÓN ===")
    regiones = list(CONFIG_LIGAS.keys())
    for i, region in enumerate(regiones, 1): print(f" {i} - {region}")
    
    opcion_reg = input("\nSelecciona el número de región: ").strip()
    
    if opcion_reg.isdigit() and 1 <= int(opcion_reg) <= len(regiones):
        region_sel = regiones[int(opcion_reg) - 1]
        print(f"\n🚀 Iniciando extracción masiva para: {region_sel}")
        
        for liga in CONFIG_LIGAS[region_sel].values():
            print(f"\n--- PROCESANDO LIGA: {liga['nombre']} ---")
            lista_temporadas = []
            
            for anio in TEMPORADAS:
                url = f"{BASE_URL}/{liga['slug']}/gesamtspielplan/wettbewerb/{liga['id_web']}/saison_id/{anio}"
                enlaces = obtener_enlaces_partidos(url)
                if enlaces:
                    datos_liga = [extraer_datos_partido(l, liga['nombre'], anio) for l in enlaces]
                    df_temp = pd.DataFrame([d for d in datos_liga if d])
                    lista_temporadas.append(df_temp)
                    print(f"  ✅ Temporada {anio} completa.")
            
            if lista_temporadas:
                df_final = pd.concat(lista_temporadas, ignore_index=True)
                df_final['region'] = region_sel
                
                TOTALS_DIR = os.path.join(DATA_RAW_DIR, 'totals')
                os.makedirs(TOTALS_DIR, exist_ok=True)
                df_final.to_csv(os.path.join(TOTALS_DIR, f"total_{liga['nombre'].lower().replace(' ', '_')}_2022_2025.csv"), index=False)
                print(f"💾 Archivo consolidado guardado.")
    else:
        print("❌ Opción inválida.")