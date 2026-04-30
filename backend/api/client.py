import requests
import time
from typing import Optional, Dict, Any
from backend.utils.logger_config import log_info, log_error

def fetch_weather_data(api_key: str, base_url: str, city: str) -> Optional[Dict[str, Any]]:
    """
    Solicita datos climáticos para el MVP.
    """
    params = {
        "key": api_key,
        "q": city,
        "lang": "es"
    }

    start_time = time.time()

    try:
        response = requests.get(
            f"{base_url}/current.json",
            params=params,
            timeout=10
        )

        latency = time.time() - start_time
        log_info(f"Latencia de la API para '{city}': {latency:.4f} segundos")

        if response.status_code == 200:
            return response.json()
        else:
            log_error(f"Error en WeatherAPI: Status {response.status_code} para la ciudad {city}")
            return None

    except requests.exceptions.RequestException as e:
        log_error(f"Fallo crítico en la conexión con WeatherAPI: {str(e)}")
        return None