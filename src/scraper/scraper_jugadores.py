import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright

def extraer_stats_partido(page, url_partido):
    # La ruta a las estadísticas detalladas
    url_stats = url_partido.replace("/index/spielbericht/", "/statistik/spielbericht/")
    page.goto(url_stats, wait_until="networkidle")
    
    try:
        # Usamos pandas para leer la tabla directamente del HTML del navegador
        # Buscamos la tabla que contiene las estadísticas de los jugadores
        html = page.content()
        dfs = pd.read_html(html)
        
        # Generalmente, la tabla de estadísticas es la primera o segunda tabla grande
        # Ajusta el índice [0] si notas que captura otra tabla
        df_stats = dfs[0] 
        
        # Limpieza básica: Filtramos filas que no tienen nombre de jugador
        df_stats = df_stats.dropna(how='all')
        
        return df_stats
    except Exception as e:
        print(f"   > Error al extraer estadísticas: {e}")
        return None

def run_stats_scraper():
    # Configuración de carpetas
    ruta_carpeta = os.path.join("data", "raw", "players")
    os.makedirs(ruta_carpeta, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # (Aquí repetirías la lógica de navegación a los partidos que ya tienes)
        # Para el ejemplo, supongamos que ya tienes tu lista de URLs de partidos
        # ...
        
        print(f"📂 Datos guardados en: {ruta_carpeta}")
        # Ejemplo de guardado:
        # df_stats.to_csv(os.path.join(ruta_carpeta, "partido_stats_123.csv"), index=False)

if __name__ == "__main__":
    run_stats_scraper()