import logging
from typing import Dict, Any, Optional
from backend.core.weather_records import create_weather_record

def normalize_weather_data(raw_data: Dict[str, Any], zone: str, source: str = "WeatherAPI") -> Optional[Dict[str, Any]]:
    """
    Normaliza datos climáticos de la API y los pasa a create_weather_record.
    """
    try:
        # Extraemos las secciones principales de la respuesta de la API
        location = raw_data["location"]
        current = raw_data["current"]

        # Retornamos la llamada a la función de molde con los datos limpios
        return create_weather_record(
            city=location.get("name", ""),
            zone=zone,
            temperature_c=current.get("temp_c", 0.0),
            humidity_pct=current.get("humidity", 0.0),
            wind_kph=current.get("wind_kph", 0.0),
            rain_mm=current.get("precip_mm", 0.0),
            source=source,
            timestamp=current.get("last_updated")
        )

    except (KeyError, TypeError) as e:
        logging.error(f"Error al normalizar datos climáticos: {e}")
        return None


