import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os
import random

TORNEOS = {
    "CL": {"nombre": "Champions League", "slug": "uefa-champions-league"},
    "CLI": {"nombre": "Copa Libertadores", "slug": "copa-libertadores"}
    # Puedes añadir el resto aquí
}

def obtener_datos_partido(page, url_partido):
    url_ali = url_partido.replace("/index/spielbericht/", "/aufstellung/spielbericht/")
    
    # Navegación con pausa aleatoria para no parecer bot
    time.sleep(random.uniform(3, 6)) 
    page.goto(url_ali, wait_until="networkidle") 
    
    try:
        # Aumentamos el timeout y usamos un selector más general si el anterior falla
        page.wait_for_selector(".sb-teamNames", timeout=15000)
        
        # Extracción más robusta
        equipos = page.eval_on_selector_all(".sb-teamNames a", "es => es.map(e => e.innerText)")
        if len(equipos) < 2: return None
        
        local, visitante = equipos[0], equipos[1]
        
        # En la página de alineaciones, los jugadores suelen estar en tablas con clase 'items'
        # o en contenedores específicos. Probemos este selector más genérico:
        jugadores = page.eval_on_selector_all("a[href*='/spieler/']", "es => es.map(e => e.innerText.trim())")
        
        # Transfermarkt lista titulares y suplentes. Vamos a tomar solo los primeros 22
        # (11 de cada uno si están ordenados así)
        if len(jugadores) < 22: return None
        
        data = {"partido": url_partido, "equipo_local": local, "equipo_visitante": visitante}
        
        # Mapeo simple de los primeros 22 encontrados
        for i in range(11):
            data[f"local_jugador_{i+1}"] = jugadores[i]
            data[f"visitante_jugador_{i+1}"] = jugadores[i+11]
            
        return data
    except Exception as e:
        print(f"   > Error real en {url_partido}: {e}")
        return None

def run_scrapper():
    ruta_carpeta = os.path.join("data", "raw", "games", "tournaments")
    os.makedirs(ruta_carpeta, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0")
        
        for id_torneo, info in TORNEOS.items():
            page = context.new_page()
            url = f"https://www.transfermarkt.com/{info['slug']}/gesamtspielplan/pokalwettbewerb/{id_torneo}"
            page.goto(url, wait_until="domcontentloaded")
            
            # Extraer enlaces
            enlaces = page.eval_on_selector_all("a[href*='/spielbericht/']", "es => es.map(e => e.href)")
            enlaces = list(set(enlaces))[:3] # Procesamos 3 para prueba
            
            resultados = []
            for url_partido in enlaces:
                print(f"🔄 Procesando: {url_partido}")
                datos = obtener_datos_partido(page, url_partido)
                if datos:
                    resultados.append(datos)
                time.sleep(2)
            
            # Guardado final
            if resultados:
                df = pd.DataFrame(resultados)
                df.to_csv(os.path.join(ruta_carpeta, f"data_{id_torneo}.csv"), index=False)
                print(f"✅ Guardado archivo estructurado para {info['nombre']}")
            
            page.close()
        browser.close()

if __name__ == "__main__":
    run_scrapper()