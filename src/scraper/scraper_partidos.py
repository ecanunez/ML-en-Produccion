import os
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from funciones import extraer_datos_partido
from funciones import obtener_enlaces_partidos

# 1. CONSTANTES Y CONFIGURACIÓN DE RUTAS
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SEASON_DIR = os.path.join(BASE_DIR, "data", "raw", "games", "seasons")
os.makedirs(SEASON_DIR, exist_ok=True)

BASE_URL = "https://www.transfermarkt.es"
TEMPORADAS = [2022, 2023, 2024, 2025]

CONFIG_LIGAS = {
    "Europa": {
            "1": {"nombre": "LaLiga", "id_web": "ES1", "slug": "laliga"},
            "2": {"nombre": "Premier League", "id_web": "GB1", "slug": "premier-league"},
            "3": {"nombre": "Bundesliga", "id_web": "L1", "slug": "bundesliga"},
            "4": {"nombre": "Serie A", "id_web": "IT1", "slug": "serie-a"},
            "5": {"nombre": "Ligue 1", "id_web": "FR1", "slug": "ligue-1"},
            "6": {"nombre": "Primeira Liga", "id_web": "PO1", "slug": "liga-nos"},
            "7": {"nombre": "Eredivisie", "id_web": "NL1", "slug": "eredivisie"},
            "8": {"nombre": "Jupiler Pro League", "id_web": "BE1", "slug": "jupiler-pro-league"},
            "9": {"nombre": "Süper Lig", "id_web": "TR1", "slug": "super-lig"},
            "10": {"nombre": "Chance Liga", "id_web": "CZ1", "slug": "chance-liga"}
},
    "Sudamérica": {
        "1": {"nombre": "Brasileirao", "id_web": "BRA1", "slug": "campeonato-brasileiro-serie-a"},
        "2": {"nombre": "Liga Profesional Argentina", "id_web": "AR1N", "slug": "liga-profesional-de-futbol"},
        "3": {"nombre": "Bolivia División Profesional", "id_web": "BODP", "slug": "division-profesional"},
        "4": {"nombre": "Chile Primera División", "id_web": "CLPD", "slug": "primera-division"},
        "5": {"nombre": "Colombia Primera A", "id_web": "COAA", "slug": "primera-a"},
        "6": {"nombre": "Ecuador LigaPro", "id_web": "ECP1", "slug": "ligapro"},
        "7": {"nombre": "Paraguay Primera División", "id_web": "PAR1", "slug": "primera-division"},
        "8": {"nombre": "Perú Liga 1", "id_web": "PEL1", "slug": "liga-1"},
        "9": {"nombre": "Uruguay Primera División", "id_web": "URU1", "slug": "primera-division"},
        "10": {"nombre": "Venezuela Primera División", "id_web": "VFP1", "slug": "primera-division"}
    },
    "Norteamérica": {
        "1": {"nombre": "Major League Soccer", "id_web": "MLS1", "slug": "major-league-soccer"},
        "2": {"nombre": "Liga MX Clausura", "id_web": "MEX1", "slug": "liga-mx-clausura"},
        "3": {"nombre": "Liga MX Apertura", "id_web": "MEX1", "slug": "liga-mx-apertura"}
    },
    "Asia": {
        "1": {"nombre": "Saudi Pro League", "id_web": "SA1", "slug": "saudi-pro-league"},
        "2": {"nombre": "J1 League", "id_web": "JAP1", "slug": "j1-league"},
        "3": {"nombre": "K-League 1", "id_web": "KOR1", "slug": "k-league-1"}
    },
    "África": {
        "1": {"nombre": "Egipto Premier League", "id_web": "EGY1", "slug": "egyptian-premier-league"},
        "2": {"nombre": "Botola Pro", "id_web": "MAR1", "slug": "botola-pro"},
        "3": {"nombre": "Túnez Ligue 1", "id_web": "TUN1", "slug": "ligue-1-professionnelle-1"},
        "4": {"nombre": "Linafoot", "id_web": "COD1", "slug": "linafoot"}
    }
}

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
            
            # CONTROL CRÍTICO: Forzamos flags específicos de escritorio y desactivamos emulación táctil
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                viewport={"width": 1440, "height": 900},
                is_mobile=False,
                has_touch=False
            )
            page = context.new_page()
            
            for liga in CONFIG_LIGAS[region_sel].values():
                print(f"\n--- PROCESANDO LIGA: {liga['nombre']} ---")
                
                for anio in TEMPORADAS:
                    print(f" > Procesando {anio}...")
                    url = f"{BASE_URL}/{liga['slug']}/gesamtspielplan/wettbewerb/{liga['id_web']}/saison_id/{anio}"
                    
                    enlaces = obtener_enlaces_partidos(url, page)
                    datos_temporada = []
                    
                    if enlaces:
                        for idx, link in enumerate(enlaces, 1):
                            datos = extraer_datos_partido(link, page, liga['nombre'], anio, region_sel)
                            if datos:
                                datos_temporada.append(datos)
                            
                            if idx % 50 == 0:
                                print(f"   ... Procesados {idx}/{len(enlaces)} partidos.")
                        
                        if datos_temporada:
                            df_temp = pd.DataFrame(datos_temporada)
                            file_name = f"{liga['nombre'].lower().replace(' ', '_')}_{anio}.csv"
                            destino_final = os.path.join(SEASON_DIR, file_name)
                            df_temp.to_csv(destino_final, index=False)
                            print(f"   ✅ ¡Temporada {anio} guardada con éxito! -> {file_name}")
                        else:
                            print(f"   ⚠️ No se lograron extraer datos válidos para la temporada {anio}.")
                    else:
                        print(f"   ⚠️ No se encontraron enlaces para la temporada {anio}.")
            
            browser.close()
            print("\n🏁 Proceso de scraping completado de manera limpia.")
    else:
        print("❌ Opción inválida.")