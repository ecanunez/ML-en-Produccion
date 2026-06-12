import os
import pandas as pd

# CONSTANTES Y CONFIGURACIÓN (Deben coincidir con las carpetas del scraper)
DATA_RAW_DIR = os.path.join("data", "raw", "games")
SEASON_DIR = os.path.join(DATA_RAW_DIR, 'seasons')
TOTALS_DIR = os.path.join(DATA_RAW_DIR, 'totals')
os.makedirs(TOTALS_DIR, exist_ok=True)

TEMPORADAS = [2024, 2025]

# Mantenemos el diccionario para saber qué ligas buscar según la región
CONFIG_LIGAS = {
    "Europa": {
        #"1": {"nombre": "LaLiga", "id_web": "ES1", "slug": "laliga"},
        #"2": {"nombre": "Premier League", "id_web": "GB1", "slug": "premier-league"},
        #"3": {"nombre": "Serie A", "id_web": "IT1", "slug": "serie-a"},
        #"4": {"nombre": "Bundesliga", "id_web": "L1", "slug": "bundesliga"},
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

def consolidar_region(region_sel):
    print(f"\n📦 Iniciando procesamiento y consolidación para: {region_sel}")
    
    for liga in CONFIG_LIGAS[region_sel].values():
        archivos_temporada = []
        nombre_liga_slug = liga['nombre'].lower().replace(' ', '_')
        
        # Buscar en el disco los CSV de cada año creados por el scraper
        for anio in TEMPORADAS:
            file_name = f"{nombre_liga_slug}_{anio}.csv"
            path_archivo = os.path.join(SEASON_DIR, file_name)
            
            if os.path.exists(path_archivo):
                try:
                    df_temp = pd.read_csv(path_archivo)
                    archivos_temporada.append(df_temp)
                    print(f" > Cargado con éxito: {file_name}")
                except Exception as e:
                    print(f" ⚠️ Error leyendo el archivo {file_name}: {e}")
            else:
                print(f" 🚫 Archivo ausente en disco (saltando): {file_name}")
        
        # Unificar si existen datos
        if archivos_temporada:
            df_final = pd.concat(archivos_temporada, ignore_index=True)
            df_final['region'] = region_sel
            
            output_final = os.path.join(TOTALS_DIR, f"total_{nombre_liga_slug}_2024_2025.csv")
            df_final.to_csv(output_final, index=False)
            print(f"💾 ARCHIVO CONSOLIDADO GUARDADO: {output_final}\n")
        else:
            print(f"❌ No se encontraron datos para la liga: {liga['nombre']}\n")

if __name__ == "__main__":
    print("\n=== PROCESADOR DE DATOS: CONSOLIDACIÓN ===")
    regiones = list(CONFIG_LIGAS.keys())
    for i, region in enumerate(regiones, 1): 
        print(f" {i} - {region}")
        
    opcion_reg = input("\n¿De qué región deseas consolidar los datos existentes?: ").strip()
    
    if opcion_reg.isdigit() and 1 <= int(opcion_reg) <= len(regiones):
        region_sel = regiones[int(opcion_reg) - 1]
        consolidar_region(region_sel)
        print("🏁 Fin del procesamiento.")
    else:
        print("❌ Opción inválida.")


# Definir la ruta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOTALS_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'games', 'totals')

def procesar_todas_las_ligas():
    print("=== Iniciando Módulo de Procesamiento Multiliga ===")
    
    if not os.path.exists(TOTALS_DIR) or not os.listdir(TOTALS_DIR):
        print(f"❌ La carpeta de totales está vacía o no existe: {TOTALS_DIR}")
        return None

    dataframes_ligas = []
    
    # Recorrer todos los archivos CSV
    for archivo in os.listdir(TOTALS_DIR):
        if archivo.endswith('.csv'):
            ruta_completa = os.path.join(TOTALS_DIR, archivo)
            print(f"📖 Leyendo: {archivo}...")
            
            try:
                # Usamos dtype=str para evitar errores con nombres o ids que parezcan números
                df_liga = pd.read_csv(ruta_completa, dtype=str)
                dataframes_ligas.append(df_liga)
            except Exception as e:
                print(f"⚠️ Error al leer {archivo}: {e}")

    if not dataframes_ligas:
        print("❌ No se pudo cargar ningún archivo CSV válido.")
        return None

    # Consolidación
    df_maestro = pd.concat(dataframes_ligas, ignore_index=True)
    
    print("\n==============================================")
    print("✅ ¡ÉXITO! Combinación multiliga completada.")
    print(f"📊 Total de partidos acumulados: {len(df_maestro)}")
    
    # Análisis rápido de regiones recién agregadas
    if 'region' in df_maestro.columns:
        resumen = df_maestro['region'].value_counts()
        print("\n--- Distribución por Regiones ---")
        print(resumen)
    
    print("==============================================")
    return df_maestro

if __name__ == "__main__":
    df_global = procesar_todas_las_ligas()