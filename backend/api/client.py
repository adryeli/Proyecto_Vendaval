import requests
import time
from typing import Optional, Dict, Any
# Importamos tus funciones de log personalizadas
from backend.utils.logger_config import log_info, log_error

def fetch_weather_data(api_key: str, base_url: str, city: str) -> Optional[Dict[str, Any]]:
    """
    Solicita datos climáticos para el MVP.
    Mide la latencia y la registra usando log_info.
    """
    params = {
        "key": api_key,
        "q": city,
        "lang": "es"
    }

    # Medimos el tiempo de inicio
    start_time = time.time()

    try:
        # Petición simple (MVP)
        response = requests.get(
            f"{base_url}/current.json",
            params=params,
            timeout=10
        )

        # Medición y log de latencia según tus instrucciones
        latency = time.time() - start_time
        log_info(f"Latencia de la API para '{city}': {latency:.4f} segundos")

        # Verificación del status code
        if response.status_code == 200:
            return response.json()
        else:
            log_error(f"Error en WeatherAPI: Status {response.status_code} para la ciudad {city}")
            return None

    except requests.exceptions.RequestException as e:
        # Registro de error en caso de fallo de red/timeout
        log_error(f"Fallo crítico en la conexión con WeatherAPI: {str(e)}")
        return None
