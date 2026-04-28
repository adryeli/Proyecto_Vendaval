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
        """
        Estrategia para Open-Meteo.
        Usa una API de Geocodificación para traducir la ciudad a coordenadas dinámicamente.
        """
        # 1. FASE DE GEOCODIFICACIÓN: Traducir Ciudad -> Coordenadas
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,        # Solo queremos el resultado más relevante
            "language": "es",
            "format": "json"
        }
        
        try:
            geo_response = requests.get(geo_url, params=geo_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            # Verificamos si la API realmente encontró la ciudad
            if "results" not in geo_data or len(geo_data["results"]) == 0:
                print(f"❌ Error: Open-Meteo no encontró coordenadas para '{city}'.")
                return None
                
            # Extraemos latitud y longitud
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red al buscar coordenadas de '{city}': {e}")
            return None

        # 2. FASE DEL CLIMA: Pedir datos con las coordenadas obtenidas
        endpoint = f"{self.openmeteo_url}/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        
        try:
            response = requests.get(endpoint, params=weather_params, timeout=10)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red con Open-Meteo al obtener el clima: {e}")
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