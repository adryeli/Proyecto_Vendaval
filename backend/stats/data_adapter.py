import pandas as pd
import json
import os
from datetime import datetime

# Rutas centralizadas para evitar errores de mantenimiento
CACHE_PATH = "data/weather_cache.json"
MANUAL_PATH = "data/manual_records.json"

def get_raw_history() -> list:
    """
    Lee los archivos JSON y devuelve una lista plana de diccionarios.
    Esta es la base para todas las demás funciones.
    """
    all_data = []
    
    for path in [CACHE_PATH, MANUAL_PATH]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    # Si el contenido es un dict (como en weather_cache.json con claves compuestas)
                    if isinstance(content, dict):
                        all_data.extend(content.values())
                    # Si el contenido es una lista (formato alternativo)
                    elif isinstance(content, list):
                        all_data.extend(content)
            except (json.JSONDecodeError, IOError):
                continue
                
    return all_data

def get_combined_data() -> pd.DataFrame:
    """
    Retorna un DataFrame de Pandas con todos los datos.
    ESENCIAL PARA: cyber_dashboard.py
    """
    data = get_raw_history()
    if not data:
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    
    # Limpieza y conversión vital para el Dashboard
    if 'timestamp' in df.columns:
        # Convertimos a datetime y quitamos el timezone para evitar errores en Matplotlib
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        # Ordenamos por fecha para que las gráficas tengan sentido
        df = df.sort_values('timestamp')
        
    return df

def get_available_cities() -> list:
    """
    Devuelve una lista única y ordenada de ciudades con datos.
    Útil para el selector del Dashboard y menús de consola.
    """
    data = get_raw_history()
    if not data:
        return []
    
    ciudades = {record['city'] for record in data if 'city' in record}
    # Ordenamos respetando tildes (Ávila antes que Barcelona)
    return sorted(list(ciudades), 
                  key=lambda x: x.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U'))

def get_latest_record(city: str = None) -> dict:
    """
    Devuelve el registro más reciente. Si se pasa 'city', filtra por ella.
    """
    df = get_combined_data()
    if df.empty:
        return {}
    
    if city:
        df = df[df['city'] == city]
        
    if df.empty:
        return {}
        
    # Retornamos el último registro como diccionario
    return df.iloc[-1].to_dict()

def get_comparative_data(city: str) -> dict:
    """
    Prepara la comparativa exigida por el Ayuntamiento: Manual vs API.
    Retorna el último de cada fuente para una ciudad.
    """
    df = get_combined_data()
    if df.empty:
        return {"manual": None, "api": None}
    
    city_data = df[df['city'] == city]
    
    manual = city_data[city_data['source'] == 'Manual'].tail(1)
    api = city_data[city_data['source'] == 'WeatherAPI'].tail(1)
    
    return {
        "manual": manual.to_dict('records')[0] if not manual.empty else None,
        "api": api.to_dict('records')[0] if not api.empty else None
    }

def get_data_by_source(source: str) -> list:
    """
    Filtra el histórico por origen (Manual o WeatherAPI).
    """
    data = get_raw_history()
    return [r for r in data if r.get('source') == source]