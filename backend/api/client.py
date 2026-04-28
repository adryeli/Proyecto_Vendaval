import os
import requests
from dotenv import load_dotenv

class ApiClient:
    """
    Cliente meteorológico flexible. 
    Capaz de usar múltiples proveedores (WeatherAPI u Open-Meteo) sin cambiar de código.
    """
    def __init__(self):
        load_dotenv()
        
        # Leemos el interruptor maestro
        self.active_api = os.getenv("ACTIVE_API", "open-meteo").lower()
        
        # Leemos las credenciales de ambos
        self.weatherapi_key = os.getenv("WEATHERAPI_KEY")
        self.weatherapi_url = os.getenv("WEATHERAPI_BASE_URL")
        self.openmeteo_url = os.getenv("OPENMETEO_BASE_URL")
        
        # Validaciones de seguridad básicas
        if self.active_api == "weatherapi" and not self.weatherapi_key:
            raise ValueError("❌ ERROR: WeatherAPI está activo pero falta WEATHERAPI_KEY en .env")

    def get_current_weather(self, city: str):
        """
        Método Director (Enrutador). Decide a qué proveedor llamar según el .env.
        """
        if self.active_api == "open-meteo":
            return self._get_from_open_meteo(city)
        elif self.active_api == "weatherapi":
            return self._get_from_weatherapi(city)
        else:
            print(f"❌ Error: El proveedor '{self.active_api}' no está soportado.")
            return None

    # --- MÉTODOS OBREROS (Privados) ---

    def _get_from_open_meteo(self, city: str):
        """Estrategia para Open-Meteo (Usa coordenadas)"""
        coordenadas = {
            "Madrid": {"lat": 40.4165, "lon": -3.7026},
            "Barcelona": {"lat": 41.3888, "lon": 2.1590},
            "Valencia": {"lat": 39.4697, "lon": -0.3774}
        }
        
        if city not in coordenadas:
            print(f"❌ Error: La ciudad '{city}' no está en nuestro diccionario de Open-Meteo.")
            return None

        endpoint = f"{self.openmeteo_url}/forecast"
        params = {
            "latitude": coordenadas[city]["lat"],
            "longitude": coordenadas[city]["lon"],
            "current_weather": True
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red con Open-Meteo: {e}")
            return None

    def _get_from_weatherapi(self, city: str):
        """Estrategia para WeatherAPI (Usa el nombre de la ciudad)"""
        endpoint = f"{self.weatherapi_url}/current.json"
        params = {
            "key": self.weatherapi_key,
            "q": city,
            "lang": "es"
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red con WeatherAPI: {e}")
            return None