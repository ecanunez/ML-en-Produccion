import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

print("=== MÓDULO 1: SCRAPER COMPLETO DE PRODUCCIÓN (TODOS LOS PARTIDOS) ===")

# 1. Configuración de rutas de almacenamiento
DATA_RAW_DIR = os.path.join("data", "raw", "games")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

BASE_URL = "https://www.transfermarkt.es"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Lista de años (temporadas) que vamos a recopilar
TEMPORADAS = [2022, 2023, 2024, 2025]

# Mapeo de ligas con su ID interno de Transfermarkt
CONFIG_LIGAS = {
    "1": {"nombre": "LaLiga", "id_web": "ES1"},
    "2": {"nombre": "Premier League", "id_web": "GB1"},
    "3": {"nombre": "Serie A", "id_web": "IT1"},
    "4": {"nombre": "Bundesliga", "id_web": "L1"},
    "5": {"nombre": "Ligue 1", "id_web": "FR1"},
    "6": {"nombre": "Liga Portugal", "id_web": "PO1"},
    "7": {"nombre": "MLS", "id_web": "MLS1"},
    "8": {"nombre": "Brasileirao", "id_web": "BRA1"}
}

def obtener_enlaces_partidos(url_calendario):
    try:
        response = requests.get(url_calendario, headers=HEADERS, timeout=15)
        if response.status_code != 200: return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        enlaces_partidos = []
        
        for link in soup.find_all("a", class_="ergebnis-link"):
            href = link.get("href")
            if href and "/spielbericht/" in href:
                enlaces_partidos.append(BASE_URL + href)
                
        return list(dict.fromkeys(enlaces_partidos))
    except Exception:
        return []

def extraer_datos_partido(url_partido, nombre_liga, anio_temporada):
    try:
        response = requests.get(url_partido, headers=HEADERS, timeout=15)
        if response.status_code != 200: return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        equipos = soup.find_all("nobr")
        if len(equipos) < 2: return None
        eq_local = equipos[0].text.strip()
        eq_visitante = equipos[1].text.strip()
        
        marcador_box = soup.find("div", class_="ergebnis-box")
        resultado = marcador_box.text.strip() if marcador_box else "0:0"
        
        bloques = soup.find_all("div", class_="large-6 columns")
        titulares_local = []
        titulares_vis = []
        
        if len(bloques) > 0 and bloques[0].find("table"):
            for fila in bloques[0].find("table").find_all("td", class_="hauptlink"):
                nombre = fila.text.strip()
                if nombre and nombre not in titulares_local: titulares_local.append(nombre)
                
        if len(bloques) > 1 and bloques[1].find("table"):
            for fila in bloques[1].find("table").find_all("td", class_="hauptlink"):
                nombre = fila.text.strip()
                if nombre and nombre not in titulares_vis: titulares_vis.append(nombre)
                
        registro = {
            "liga": nombre_liga,
            "temporada": anio_temporada,
            "equipo_local": eq_local,
            "equipo_visitante": eq_visitante,
            "resultado": resultado
        }
        
        for i, jug in enumerate(titulares_local[:11]):
            registro[f"local_jugador_{i+1}"] = jug
        for i, jug in enumerate(titulares_vis[:11]):
            registro[f"visitante_jugador_{i+1}"] = jug
            
        return registro
    except Exception:
        return None

if __name__ == "__main__":
    print("\n¿Qué liga deseas recopilar históricamente (2022-2025)?")
    for clave, info in CONFIG_LIGAS.items():
        print(f" {clave} - {info['nombre']}")
        
    opcion = input("\nSelecciona una opción (1 al 8): ").strip()
    
    if opcion in CONFIG_LIGAS:
        liga = CONFIG_LIGAS[opcion]
        print(f"\n🚀 Iniciando extracción masiva para: {liga['nombre']}")
        
        archivos_temporadas = []
        
        for anio in TEMPORADAS:
            print(f"\n--- TRABAJANDO TEMPORADA {anio} ---")
            url_calendario = f"{BASE_URL}/la-liga/gesamtspielplan/wettbewerb/{liga['id_web']}/saison_id/{anio}"
            
            enlaces = obtener_enlaces_partidos(url_calendario)
            
            if enlaces:
                print(f"✅ Se detectaron {len(enlaces)} partidos en total. Descargando alineaciones reales...")
                dataset_partidos = []
                
                # Eliminamos el [:5] -> Ahora va por TODO el calendario del año
                for i, url in enumerate(enlaces):
                    # Un print simple cada 20 partidos para saber que sigue vivo sin saturar la pantalla
                    if i % 20 == 0 or i == len(enlaces) - 1:
                        print(f"   🔄 Progresando: {i}/{len(enlaces)} partidos procesados...")
                        
                    datos = extraer_datos_partido(url, liga["nombre"], anio)
                    if datos:
                        dataset_partidos.append(datos)
                    time.sleep(0.5) # Pausa segura para no saturar al servidor
                
                # Guardamos el archivo individual de ese año
                df_anio = pd.DataFrame(dataset_partidos)
                nombre_archivo = f"historico_{liga['nombre'].lower().replace(' ', '_')}_{anio}_raw.csv"
                csv_path = os.path.join(DATA_RAW_DIR, nombre_archivo)
                df_anio.to_csv(csv_path, index=False)
                print(f"💾 Temporada {anio} guardada ({len(df_anio)} partidos).")
                archivos_temporadas.append(df_anio)
            else:
                print(f"⚠ No se pudieron obtener enlaces para la temporada {anio}.")
                
        # --- CONSOLIDACIÓN FINAL ---
        if archivos_temporadas:
            print("\n🔄 Combinando todas las temporadas en un solo dataset unificado...")
            df_final = pd.concat(archivos_temporadas, ignore_index=True)
            
            # Guardamos el archivo definitivo de la liga completa
            nombre_unificado = f"total_{liga['nombre'].lower().replace(' ', '_')}_2022_2025.csv"
            ruta_unificada = os.path.join(DATA_RAW_DIR, nombre_unificado)
            df_final.to_csv(ruta_unificada, index=False)
            
            print("\n=======================================================")
            print(f"🎉 ¡EXTRACCIÓN TOTAL COMPLETADA!")
            print(f"📊 Dataset maestro unificado ({len(df_final)} partidos):")
            print(f"📁 {ruta_unificada}")
            print("=======================================================")
            
    else:
        print("❌ Opción inválida.")