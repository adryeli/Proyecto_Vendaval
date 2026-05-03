import pytest
from unittest.mock import patch, MagicMock
from backend.api.client import fetch_weather_data

# Simulamos (Mock) la sesión que creamos en el cliente
@patch('backend.api.client._session.get')
def test_fetch_weather_data_success(mock_get):
    """Prueba una respuesta exitosa (200 OK)"""

    # Configuramos el simulador para que devuelva un 200 y un JSON de prueba
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"location": {"name": "Havana"}, "current": {"temp_c": 28}}
    mock_get.return_value = mock_response

    # Ejecutamos la función
    result = fetch_weather_data("fake_key", "http://api.test", "Havana")

    # Verificaciones (Assertions)
    assert result is not None
    assert result["location"]["name"] == "Havana"
    assert mock_get.called # Verificamos que se llamó a la sesión

@patch('backend.api.client._session.get')
def test_fetch_weather_data_error(mock_get):
    """Prueba el comportamiento cuando la API falla (ej. 404)"""

    # Simulamos un error de "Ciudad no encontrada"
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = fetch_weather_data("fake_key", "http://api.test", "InvalidCity")

    # Debe devolver None según nuestra lógica de client.py
    assert result is None

@patch('backend.api.client._session.get')
def test_fetch_weather_data_exception(mock_get):
    """Prueba qué pasa si hay un fallo de red total"""

    # Simulamos una excepción de requests (como si se cortara internet)
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError()

    result = fetch_weather_data("fake_key", "http://api.test", "Havana")

    # Debe manejar la excepción y devolver None
    assert result is None
