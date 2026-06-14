import os
import glob
import pandas as pd

# CONSTANTES Y CONFIGURACIÓN
DATA_RAW_DIR = os.path.join("data", "raw", "games")
SEASON_DIR = os.path.join(DATA_RAW_DIR, "seasons")
TOTALS_DIR = os.path.join(DATA_RAW_DIR, 'totals')
os.makedirs(TOTALS_DIR, exist_ok=True)

def consolidar_todo_lo_existente():
    print("🔍 Escaneando la carpeta 'seasons' en busca de datos...")
    
    # 1. Buscar todos los archivos .csv en la carpeta seasons
    archivos_csv = glob.glob(os.path.join(SEASON_DIR, "*.csv"))
    
    if not archivos_csv:
        print(f"❌ No se encontraron archivos .csv en la ruta: {SEASON_DIR}")
        return

    # 2. Agrupar los archivos por su nombre de liga
    ligas_detectadas = {}
    
    for ruta_archivo in archivos_csv:
        nombre_archivo = os.path.basename(ruta_archivo)  # Ejemplo: "ligue_1_2024.csv"
        partes = nombre_archivo.rsplit("_", 1)           # Separa el año: ["ligue_1", "2024.csv"]
        
        if len(partes) == 2:
            nombre_liga_slug = partes[0]  # "ligue_1"
            
            if nombre_liga_slug not in ligas_detectadas:
                ligas_detectadas[nombre_liga_slug] = []
            
            ligas_detectadas[nombre_liga_slug].append(ruta_archivo)

    print(f"📈 Se detectaron datos para {len(ligas_detectadas)} ligas distintas.\n")

    # 3. Consolidar cada liga detectada sin añadir columnas extra
    for nombre_liga_slug, lista_archivos in ligas_detectadas.items():
        print(f"📦 Consolidando liga: '{nombre_liga_slug}' (Uniendo {len(lista_archivos)} temporadas)...")
        archivos_a_unir = []
        
        for archivo in lista_archivos:
            try:
                df_temp = pd.read_csv(archivo)
                archivos_a_unir.append(df_temp)
                print(f"   -> Cargado: {os.path.basename(archivo)}")
            except Exception as e:
                print(f"   ⚠️ Error al leer {os.path.basename(archivo)}: {e}")
        
        if archivos_a_unir:
            # Concatenamos de forma pura las temporadas de esta liga
            df_final = pd.concat(archivos_a_unir, ignore_index=True)
            
            # Guardamos el archivo final tal y como venía estructurado originalmente
            output_final = os.path.join(TOTALS_DIR, f"total_{nombre_liga_slug}.csv")
            df_final.to_csv(output_final, index=False)
            print(f"💾 ¡GUARDADO!: {output_final}\n")

if __name__ == "__main__":
    print("=== PROCESADOR AUTOMÁTICO (SOLO UNIFICACIÓN) ===")
    consolidar_todo_lo_existente()
    print("🏁 Proceso terminado. Archivos totales creados.")


import glob
import pandas as pd

archivos = glob.glob(
    "data/raw/games/international_competitions/*.csv"
)

df = pd.concat(
    [pd.read_csv(f) for f in archivos],
    ignore_index=True
)

print(df.shape)