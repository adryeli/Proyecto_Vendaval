"""
Módulo de Persistencia JSON - Proyecto Vendaval (Barlovento Data)
...
"""

import json
import os
from typing import Optional, Dict

# Rutas para cada origen
API_FILE_PATH = "data/weather_cache.json"
MANUAL_FILE_PATH = "data/manual_records.json"

# Mantenemos la ruta por defecto para compatibilidad con llamadas explícitas
DEFAULT_FILE_PATH = API_FILE_PATH


def ensure_file_exists(file_path: str) -> None:
    """Crea carpeta y archivo si no existen."""
    directorio = os.path.dirname(file_path)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f)


def save_record(record: dict, file_path: Optional[str] = None) -> bool:
    """
    Guarda un registro en el archivo correspondiente a su origen.
    
    - Si se proporciona file_path, se usa esa ruta (compatibilidad).
    - Si no, se elige automáticamente:
        * source == 'Manual' → manual_records.json
        * Cualquier otro → weather_cache.json
    """
    # Determinar archivo destino
    if file_path is None:
        source = record.get('source', 'WeatherAPI')
        file_path = MANUAL_FILE_PATH if source == 'Manual' else API_FILE_PATH

    ensure_file_exists(file_path)

    # Cargar datos existentes
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Clave compuesta única (timestamp + zone + city)
    clave = f"{record['timestamp']}_{record['zone']}_{record['city']}"
    data[clave] = record

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return True


def get_all_records(file_path: Optional[str] = None) -> dict:
    """
    Devuelve el diccionario con todos los registros.
    
    - Si se pasa file_path, lee solo ese archivo.
    - Si no, combina los registros de weather_cache.json y manual_records.json.
    """
    if file_path is not None:
        # Comportamiento original explícito
        ensure_file_exists(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # --- Modo combinado (sin ruta explícita) ---
    registros = {}

    # Cargar API
    ensure_file_exists(API_FILE_PATH)
    try:
        with open(API_FILE_PATH, 'r', encoding='utf-8') as f:
            registros.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Cargar Manuales (pueden sobrescribir claves si hubiera colisión, muy improbable)
    ensure_file_exists(MANUAL_FILE_PATH)
    try:
        with open(MANUAL_FILE_PATH, 'r', encoding='utf-8') as f:
            manuales = json.load(f)
            # Opcional: registrar aviso si hay claves repetidas
            comunes = set(registros.keys()) & set(manuales.keys())
            if comunes:
                from backend.utils.logger_config import log_warning
                log_warning(f"Claves duplicadas al combinar registros: {comunes}")
            registros.update(manuales)   # Los manuales prevalecen
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return registros