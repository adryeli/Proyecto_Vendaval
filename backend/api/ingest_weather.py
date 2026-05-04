import os 
import json
from dotenv import load_dotenv

from backend.api.client import fetch_weather_data 
from backend.api.normalizer import normalize_weather_data
from backend.core.alerts import evaluate_alerts
from backend.core.validator import validate_record
from backend.utils.logger_config import log_info, log_error
from backend.storage.json_repo import save_record, get_all_records

ZONE_FILE_PATH="config/zones.json"

def load_zones(file_path: str = ZONE_FILE_PATH):
    try: 
        with open (file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError) as e:
        log_error(f"Error al cargar las zonas: {e}")
        return []

def ingest_city_weather(city, zone):
    load_dotenv()
    
    base_url=os.getenv("API_BASE_URL")
    api_key=os.getenv("WEATHER_API_KEY")

    if not api_key or not base_url:
        log_error("WeatherAPI: Error de configuración -> Revise el .env")
        return None

    raw_data=fetch_weather_data(api_key, base_url, city)

    if raw_data is None:
        log_error(f"No se pudo obtener datos de {city}")
        return None

    record=normalize_weather_data(raw_data,zone)

    if record is None:
        log_error(f"Error al normalizar datos de {city}")
        return None 

    is_valid, message = validate_record(record)
    if not is_valid:
        log_error(f"Datos inválidos para {city}: {message}")
        return None

    alerts = evaluate_alerts(record)
    final_record = {
        **record,
        "alerts":alerts
    }

    save_record(final_record)

    log_info(f"Datos de {city} guardados correctamente")

    return final_record 

def ingest_zone(zone):
    records=[]
    cities=get_cities_by_zone(zone)

    for city in cities:
        record=ingest_city_weather(city,zone)
        if record:
            records.append(record)
    
    return records

def ingest_all_zones():
    zones = load_zones()
    records = []

    for zone_info in zones:
        city = zone_info.get("city")
        zone = zone_info.get("zone")
        
        if not city or not zone:
            log_error("Error en la configuración de zonas")
            continue

        record=ingest_city_weather(city, zone)

        if record:
            records.append(record)
    
    return records

    