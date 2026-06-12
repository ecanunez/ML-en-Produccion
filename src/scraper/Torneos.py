import pandas as pd
from playwright.sync_api import sync_playwright
import time

# He añadido tus nuevos torneos a la lista
TORNEOS = {
    "CL": {"nombre": "Champions League", "slug": "uefa-champions-league"},
    "CLI": {"nombre": "Copa Libertadores", "slug": "copa-libertadores"},
    "CS": {"nombre": "Copa Sudamericana", "slug": "copa-sudamericana"},
    "CCL": {"nombre": "Concacaf Champions League", "slug": "concacaf-champions-league"},
    "AFT": {"nombre": "Artemio Franchi Trophy", "slug": "artemio-franchi-trophy"},
    "CHAN": {"nombre": "African Nations Championship", "slug": "african-nations-championship"},
    "ACL1": {"nombre": "AFC Champions League", "slug": "afc-champions-league"},
    "CAF1": {"nombre": "CAF Champions League", "slug": "caf-champions-league"}
}

def extraer_jugadores(page, url_partido):
    # Intentamos navegar a la pestaña de alineaciones (Aufstellung)
    url_alineacion = url_partido.replace("/index/spielbericht/", "/aufstellung/spielbericht/")
    try:
        page.goto(url_alineacion, wait_until="networkidle", timeout=15000)
        # Extraemos nombres de jugadores mediante sus enlaces de perfil
        nombres = page.eval_on_selector_all(
            "a[href*='/spieler/']", 
            "elements => elements.map(e => e.innerText.trim())"
        )
        return list(set([n for n in nombres if n and len(n) > 2]))
    except:
        return []

def run_scrapper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for id_torneo, info in TORNEOS.items():
            print(f"\n🚀 Iniciando extracción: {info['nombre']}")
            page = browser.new_context().new_page()
            
            # Navegación al calendario
            url_calendario = f"https://www.transfermarkt.com/{info['slug']}/gesamtspielplan/pokalwettbewerb/{id_torneo}"
            page.goto(url_calendario, wait_until="networkidle")
            
            # Captura de enlaces (Selector robusto para tablas)
            enlaces = page.eval_on_selector_all("table.items a[href*='/spielbericht/']", "es => es.map(e => e.href)")
            enlaces = list(set(enlaces))
            
            print(f" > Encontrados {len(enlaces)} partidos.")
            
            resultados = []
            for url in enlaces[:5]: # Proceso rápido de 5 partidos
                nombres = extraer_jugadores(page, url)
                resultados.append({"torneo": info['nombre'], "partido": url, "jugadores": nombres})
                print(f"   > {len(nombres)} jugadores encontrados.")
                time.sleep(1) # Delay humano para evitar bloqueos
            
            # Guardado acumulativo simple
            if resultados:
                pd.DataFrame(resultados).to_csv(f"data_{id_torneo}.csv", index=False)
            
            page.close()
        browser.close()

if __name__ == "__main__":
    run_scrapper()