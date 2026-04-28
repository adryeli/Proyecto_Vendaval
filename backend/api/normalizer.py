import logging
from typing import Dict, Any, Optional
from datetime import datetime
from backend.core.weather_records import create_weather_record

def normalize_weather_data(raw_data: Dict[str, Any], zone: str, source: str = "WeatherAPI") -> Optional[Dict[str, Any]]:
    """
    Normaliza datos climáticos y genera un registro completo con ID.

    Args:
        raw_data: Datos crudos de la API
        zone: Zona geográfica
        source: Origen de los datos

    Returns:
        Diccionario con el registro climático completo (incluyendo timestamp generado)
        o None si hay error
    """
    # Validación inicial simple
    if not raw_data or not raw_data.get("current") or not raw_data.get("location"):
        logging.warning("Datos de entrada incompletos")
        return None

    try:
        # Extraer datos necesarios
        current_data = raw_data["current"]
        location_data = raw_data["location"]

        # Crear el registro usando create_weather_record
        weather_record = create_weather_record(
            city=location_data["name"],
            zone=zone,
            temperature_c=current_data["temp_c"],
            humidity_pct=current_data["humidity"],
            wind_kph=current_data["wind_kph"],
            rain_mm=current_data["precip_mm"],
            source=source,
            timestamp=current_data.get("last_updated")  # Usa el timestamp de la API si está disponible
        )

        return weather_record

    except KeyError as e:
        logging.error(f"Campo requerido no encontrado: {e}")
        return None
    except ValueError as e:
        logging.error(f"Error en formato de datos: {e}")
        return None
    except Exception as e:
        logging.error(f"Error inesperado al normalizar datos: {e}", exc_info=True)
        return None