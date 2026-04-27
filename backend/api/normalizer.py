import uuid
import logging
from typing import Dict, Any, Optional

def normalize_weather_data(raw_data: Dict[str, Any], source: str = "api") -> Optional[Dict[str, Any]]:
    """
    Transforma los datos de WeatherAPI al esquema definido en weather_records.py.
    """
    if not raw_data:
        return None

    try:
        # Mapeo directo al nuevo esquema de diccionario/JSON
        normalized_record = {
            "record_id": str(uuid.uuid4()),  # Genera un ID único para el registro
            "timestamp": raw_data["current"]["last_updated"],
            "city": raw_data["location"]["name"],
            "zone": raw_data["location"]["region"],
            "temperature_c": float(raw_data["current"]["temp_c"]),
            "humidity": float(raw_data["current"]["humidity"]),
            "wind_kph": float(raw_data["current"]["wind_kph"]),
            "rain_mm": float(raw_data["current"]["precip_mm"]), # precip_mm es el estándar de la API
            "source": source,
            "alert_level": _calculate_alert_level(raw_data["current"]["temp_c"]) # Lógica opcional
        }

        return normalized_record

    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"Error de normalización con el nuevo esquema (Fuente: {source}): {str(e)}")
        return None

def _calculate_alert_level(temp: float) -> str:
    """
    Lógica simple para determinar el nivel de alerta basado en la temperatura.
    """
    if temp > 35:
        return "high"
    elif temp > 30:
        return "medium"
    return "low"