import requests
import os

class WeatherClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url

        # 1. GESTIÓN DE SESIÓN: Creamos una sesión persistente
        # Esto reutiliza la conexión y es más eficiente (mejor performance)
        self.session = requests.Session()

        # 2. GESTIÓN DE HEADERS: Definimos los encabezados base
        # Aquí es donde el sistema se "identifica" ante el servidor
        self.session.headers.update({
            "User-Agent": "ProyectoVendaval/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        # Si pasamos una API Key, la incluimos de forma global en la sesión
        if api_key:
            self.session.headers.update({"X-API-KEY": api_key})

    def fetch_weather(self, endpoint, params=None):
        """Método simple para obtener datos usando la sesión y headers configurados"""
        url = f"{self.base_url}/{endpoint}"

        try:
            # La sesión ya incluye los headers automáticamente
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status() # Lanza error si la respuesta es mala (4xx o 5xx)
            return response.json()

        except requests.exceptions.RequestException as e:
            # Aquí podrías conectar con tu logger de backend/utils/
            print(f"[Error] Fallo en la conexión con la API: {e}")
            return None

    def close_session(self):
        """Cerramos la sesión para liberar recursos"""
        self.session.close()