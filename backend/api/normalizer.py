from datetime import datetime
from typing import Dict, Any, Optional
import logging
from backend.core.weather_record import WeatherRecord

def normalize_weather_data(raw_data: Dict[str, Any], source: str = "api") -> Optional[WeatherRecord]:
    """
    Transforma el diccionario crudo al modelo estandarizado WeatherRecord
    Permite etiquetar el origen de los datos (manual o api).
    """
    if not raw_data:
        return None

    try:
        # Extraemos y formateamos la fecha de actualización
        last_updated_str = raw_data["current"]["last_updated"]
        dt_object = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M")

        return WeatherRecord(
            location=raw_data["location"]["name"],
            region=raw_data["location"]["region"],
            country=raw_data["location"]["country"],
            lat=raw_data["location"]["lat"],
            lon=raw_data["location"]["lon"],
            temp_c=raw_data["current"]["temp_c"],
            humidity=raw_data["current"]["humidity"],
            condition=raw_data["current"]["condition"]["text"],
            last_updated=dt_object,
            source=source
        )
        
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"Error de normalización (Fuente: {source}): {str(e)}")
        return None