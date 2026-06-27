import os
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from src.scraper.scraper_utils import (
    extraer_datos_partido_internacional,
    obtener_enlaces_competicion,
)
from src.config.competition_config import (
    COMPETITIONS
)
from src.config.project_config import (
    HISTORICAL_SEASONS
)

# 1. CONSTANTES Y CONFIGURACIÓN DE RUTAS
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SEASON_DIR = os.path.join(BASE_DIR, "data", "raw", "games", "seasons")
os.makedirs(SEASON_DIR, exist_ok=True)

BASE_URL = "https://www.transfermarkt.es"
TEMPORADAS = [2022, 2023, 2024, 2025]

ligas = {
    k: v
    for k, v in COMPETITIONS.items()
    if v["region"] == "domestic"
}

url = construir_url_calendario(
    liga,
    temporada
)

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
                
                for temporada in HISTORICAL_SEASONS:
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