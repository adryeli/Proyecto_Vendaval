import pandas as pd
import json
import os

def get_combined_data() -> pd.DataFrame:
    """
    Une los datos de la API y los Manuales en un solo DataFrame
    listo para el Dashboard.
    """
    # Rutas relativas a la carpeta data
    cache_path = "data/weather_cache.json"
    manual_path = "data/manual_records.json"
    
    # Lista para acumular los datos de ambos archivos
    all_data = []
    
    # Intentamos cargar datos de la API
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            all_data.extend(json.load(f))
            
    # Intentamos cargar datos Manuales
    if os.path.exists(manual_path):
        with open(manual_path, "r", encoding="utf-8") as f:
            all_data.extend(json.load(f))
            
    if not all_data:
        return pd.DataFrame() # Devuelve tabla vacía si no hay nada
        
    df = pd.DataFrame(all_data)
    
    # Conversión vital para que el Eje X de tu gráfica funcione
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
    return df