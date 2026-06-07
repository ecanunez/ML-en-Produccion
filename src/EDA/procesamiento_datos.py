import os
import pandas as pd

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