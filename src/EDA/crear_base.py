import pandas as pd
import os

def crear_dataset_maestro():
    # Rutas a tus nuevos datos
    path = os.path.join("data", "raw")
    
    # 1. Cargamos las tablas base
    games = pd.read_csv(os.path.join(path, "games.csv"))
    appearances = pd.read_csv(os.path.join(path, "appearances.csv"))
    
    # 2. Hacemos un merge (Join) para tener info del partido + info del jugador
    # Unimos por 'game_id'
    df_master = pd.merge(appearances, games[['game_id', 'date', 'league_id']], on='game_id', how='left')
    
    # 3. Guardamos el resultado en la carpeta procesada
    ruta_proc = os.path.join("data", "processed")
    os.makedirs(ruta_proc, exist_ok=True)
    df_master.to_csv(os.path.join(ruta_proc, "dataset_final.csv"), index=False)
    
    print(f"✅ Dataset maestro creado con {len(df_master)} registros.")

if __name__ == "__main__":
    crear_dataset_maestro()