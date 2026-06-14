import pandas as pd
import os
import glob
from playwright.sync_api import sync_playwright
import time

def extraer_stats_partido(page, url_partido):
    # Convertimos la URL del partido a la de estadísticas
    url_stats = url_partido.replace("/index/spielbericht/", "/statistik/spielbericht/")
    page.goto(url_stats, wait_until="networkidle")
    
    try:
        # Extraemos las tablas de la página
        df_list = pd.read_html(page.content())
        # La tabla de estadísticas suele estar entre las primeras
        # Aquí tomamos la primera tabla que detecte Pandas con datos de jugadores
        df_stats = df_list[0] 
        return df_stats
    except Exception as e:
        print(f"   > Error al extraer estadísticas: {e}")
        return None

def run_stats_scraper():
    # 1. Rutas
    ruta_input = os.path.join("data", "raw", "games", "tournaments")
    ruta_output = os.path.join("data", "raw", "players")
    os.makedirs(ruta_output, exist_ok=True)

    # 2. Obtener lista de archivos procesados anteriormente
    archivos_partidos = glob.glob(os.path.join(ruta_input, "data_*.csv"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        for archivo in archivos_partidos:
            print(f"\n📂 Procesando archivo: {os.path.basename(archivo)}")
            df_partidos = pd.read_csv(archivo)
            
            for _, row in df_partidos.iterrows():
                url = row['partido']
                df_stats = extraer_stats_partido(page, url)
                
                if df_stats is not None:
                    # Guardamos el archivo con un nombre único por partido
                    partido_id = url.split('/')[-1]
                    ruta_salida = os.path.join(ruta_output, f"stats_{partido_id}.csv")
                    df_stats.to_csv(ruta_salida, index=False)
                    print(f"   > Guardado: {ruta_salida}")
                
                time.sleep(2) # Respeto al servidor
        
        browser.close()

if __name__ == "__main__":
    run_stats_scraper()