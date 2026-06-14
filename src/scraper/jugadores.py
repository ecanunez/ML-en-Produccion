#pip install kaggle

import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def descargar_dataset():
    # 1. Configuración de rutas
    ruta_destino = os.path.join("data", "raw", "players")
    os.makedirs(ruta_destino, exist_ok=True)
    
    # 2. Conexión a la API de Kaggle
    api = KaggleApi()
    api.authenticate()
    
    # 3. Descarga del dataset
    print("🚀 Descargando dataset desde Kaggle...")
    api.dataset_download_files('davidcariboo/player-scores', path=ruta_destino, unzip=True)
    
    print(f"✅ Dataset descargado y descomprimido en: {ruta_destino}")

if __name__ == "__main__":
    descargar_dataset()