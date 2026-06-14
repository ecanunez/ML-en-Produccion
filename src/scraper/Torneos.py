import os
import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_tournaments")
os.makedirs(SAVE_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

CONFIG = [
    {"nombre": "Champions", "id": "CL", "slug": "uefa-champions-league"},
    {"nombre": "Libertadores", "id": "CLI", "slug": "copa-libertadores"}
]

def extraer_partido(session, url):
    try:
        resp = session.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        # Buscamos el link de alineaciones
        ali_tag = soup.find("a", href=lambda x: x and "/aufstellung/spielbericht/" in x)
        if not ali_tag: return None
        
        res_ali = session.get("https://www.transfermarkt.es" + ali_tag['href'], headers=HEADERS, timeout=10)
        soup_ali = BeautifulSoup(res_ali.content, "html.parser")
        
        equipos = [t.text.strip() for t in soup_ali.select(".sb-teamNames a")]
        jugadores = [j.text.strip() for j in soup_ali.select("a.spieler-link")]
        
        if len(equipos) >= 2 and len(jugadores) >= 11:
            return {"local": equipos[0], "visitante": equipos[1]}
    except:
        return None
    return None

def run_scraper():
    temp = input("Introduce la temporada (ej. 2024): ")
    session = requests.Session()
    
    for torneo in CONFIG:
        print(f"\n🔄 Procesando {torneo['nombre']} {temp}...")
        url = f"https://www.transfermarkt.es/{torneo['slug']}/gesamtspielplan/pokalwettbewerb/{torneo['id']}/saison_id/{temp}"
        
        resp = session.get(url, headers=HEADERS, timeout=15)
        links = [f"https://www.transfermarkt.es{a['href']}" for a in BeautifulSoup(resp.content, "html.parser").select("a[href*='/spielbericht/']")]
        links = list(set(links))
        
        datos = []
        for i, link in enumerate(links):
            res = extraer_partido(session, link)
            if res:
                res['temporada'] = temp
                datos.append(res)
                print(f"  > {i+1}/{len(links)} extraído...", end="\r")
            
            # GUARDADO INTERMEDIO (Cada 10 partidos)
            if len(datos) > 0 and len(datos) % 10 == 0:
                pd.DataFrame(datos).to_csv(os.path.join(SAVE_DIR, f"{torneo['nombre']}_{temp}.csv"), index=False)
            
            time.sleep(random.uniform(2, 4))
        
        # Guardado final
        if datos:
            pd.DataFrame(datos).to_csv(os.path.join(SAVE_DIR, f"{torneo['nombre']}_{temp}.csv"), index=False)
            print(f"\n✅ FINALIZADO: {len(datos)} registros guardados en {SAVE_DIR}")

if __name__ == "__main__":
    run_scraper()