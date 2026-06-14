import pandas as pd
import glob
import os

# Obtener la ruta de la carpeta donde están los datos
# Esto busca la carpeta 'data/raw/games/totals' desde la raíz del proyecto
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(base_dir, 'data', 'raw', 'games', 'totals', '*.csv')

all_files = glob.glob(path)

if not all_files:
    print(f"No se encontraron archivos en: {path}")
else:
    print(f"Archivos encontrados: {len(all_files)}")
    # Unir todos los archivos
    df_list = [pd.read_csv(filename) for filename in all_files]
    df = pd.concat(df_list, axis=0, ignore_index=True)
    print(f"Total de registros consolidados: {len(df)}")
    print(df.head())

# 1. Limpieza de resultados
def limpiar_resultados(res):
    try:
        # Extraer goles totales (ej: 1:0)
        totales = res.split('\n')[0].split(':')
        goles_local = int(totales[0])
        goles_visita = int(totales[1])
        return goles_local, goles_visita
    except:
        return None, None

df[['goles_loc', 'goles_vis']] = df['resultado'].apply(lambda x: pd.Series(limpiar_resultados(str(x))))

# 2. Análisis de datos
print("--- Resumen de Datos ---")
print(f"Total de partidos: {len(df)}")
print(f"Jugadores 'Desconocido' en equipos: {df[df['equipo_local'] == 'Desconocido'].shape[0]}")
print("\nDistribución de Resultados:")
print(df[['goles_loc', 'goles_vis']].describe())

# 3. Identificar si hay columnas de jugadores con muchos nulos
jugadores_cols = [col for col in df.columns if 'jugador' in col]
print(f"\nCantidad de columnas de jugadores: {len(jugadores_cols)}")