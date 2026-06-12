import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os  # <--- ¡Importación necesaria!

TORNEOS = {
    "CL": {"nombre": "Champions League", "slug": "uefa-champions-league"},
    "CLI": {"nombre": "Copa Libertadores", "slug": "copa-libertadores"},
    "CS": {"nombre": "Copa Sudamericana", "slug": "copa-sudamericana"},
    "CCL": {"nombre": "Concacaf Champions League", "slug": "concacaf-champions-league"},
    "ACL1": {"nombre": "AFC Champions League", "slug": "afc-champions-league"},
    "CAF1": {"nombre": "CAF Champions League", "slug": "caf-champions-league"}
}

def run_scrapper():
    # Definir la ruta donde se guardarán los archivos
    ruta_carpeta = os.path.join("data", "raw", "games", "tournaments")
    os.makedirs(ruta_carpeta, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        
        for id_torneo, info in TORNEOS.items():
            page = context.new_page()
            url = f"https://www.transfermarkt.com/{info['slug']}/gesamtspielplan/pokalwettbewerb/{id_torneo}"
            
            print(f"\n🚀 Visitando: {info['nombre']}")
            page.goto(url, wait_until="domcontentloaded")
            
            # 1. Intentar cargar tabla, si falla, buscar pestaña "Fixtures"
            try:
                page.wait_for_selector("table.items", timeout=5000)
            except:
                print(" ⚠️ Tabla principal no cargada, buscando pestaña 'Fixtures'...")
                try:
                    page.get_by_role("link", name="Fixtures").first.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_selector("table.items", timeout=10000)
                except:
                    print(" ❌ No se pudo encontrar tabla o pestaña de partidos.")
                    page.close()
                    continue

            # 2. Extraer enlaces
            enlaces = page.eval_on_selector_all("a[href*='/spielbericht/']", "es => es.map(e => e.href)")
            enlaces = list(set(enlaces))
            print(f" > Encontrados {len(enlaces)} partidos. Procesando primeros 3...")
            
            resultados = []
            
            # 3. Procesar partidos
            for url_partido in enlaces[:3]:
                url_ali = url_partido.replace("/index/spielbericht/", "/aufstellung/spielbericht/")
                page.goto(url_ali, wait_until="domcontentloaded")
                
                try:
                    page.wait_for_selector("a[href*='/spieler/']", timeout=5000)
                    nombres = page.eval_on_selector_all("a[href*='/spieler/']", "es => es.map(e => e.innerText.trim())")
                    nombres_unicos = list(set([n for n in nombres if n and len(n) > 2]))
                    resultados.append({"partido": url_partido, "jugadores": nombres_unicos})
                    print(f"   > {len(nombres_unicos)} jugadores encontrados.")
                except:
                    print("   > No se detectaron jugadores en esta página.")
                
                time.sleep(2) 
            
            # 4. Guardado automático en la nueva ruta
            if resultados:
                ruta_completa = os.path.join(ruta_carpeta, f"data_{id_torneo}.csv")
                df = pd.DataFrame(resultados)
                df.to_csv(ruta_completa, index=False)
                print(f"✅ Guardado: {ruta_completa}")
            
            page.close()
            
        browser.close()
        print("\n🏁 Proceso finalizado.")

if __name__ == "__main__":
    run_scrapper()