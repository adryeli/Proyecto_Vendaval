import uuid
import logging
from typing import Dict, Any, Optional

def normalize_weather_data(raw_data: Dict[str, Any], source: str = "api") -> Optional[Dict[str, Any]]:
    """
    Transforma los datos de WeatherAPI al esquema de weather_records.py.
    Se elimina la lógica de alerta para manejarla en otra capa del proyecto.
    """
    if not raw_data:
        return None

    try:
        return {
            "record_id": str(uuid.uuid4()),
            "timestamp": raw_data["current"]["last_updated"],
            "city": raw_data["location"]["name"],
            "zone": raw_data["location"]["region"],
            "temperature_c": float(raw_data["current"]["temp_c"]),
            "humidity": float(raw_data["current"]["humidity"]),
            "wind_kph": float(raw_data["current"]["wind_kph"]),
            "rain_mm": float(raw_data["current"]["precip_mm"]),
            "source": source
            # alert_level eliminado según instrucciones
        }
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"Error de normalización: {str(e)}")
        return None