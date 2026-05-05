import pytest
from unittest.mock import patch
from backend.core.compare import _detectar_discrepancias, comparar_ciudad

# Registros de prueba
manual_record = {
    "city": "Madrid",
    "zone": "centro",
    "temperature_c": 20.0,
    "humidity_pct": 50.0,
    "wind_kph": 10.0,
    "timestamp": "2026-05-05 10:00",
    "source": "manual"
}

api_record = {
    "city": "Madrid",
    "zone": "centro",
    "temperature_c": 20.0,
    "humidity_pct": 50.0,
    "wind_kph": 10.0,
    "timestamp": "2026-05-05 12:00",
    "source": "WeatherAPI"
}


def test_sin_discrepancias():
    """Registros iguales no deben generar discrepancias"""
    resultado = _detectar_discrepancias(manual_record, api_record)
    assert resultado == []


def test_discrepancia_temperatura():
    """Diferencia de temperatura mayor a 3°C debe generar discrepancia"""
    actual_mod = {**api_record, "temperature_c": 25.0}  # diferencia de 5°C
    resultado = _detectar_discrepancias(manual_record, actual_mod)
    assert len(resultado) == 1
    assert "Temperatura" in resultado[0]


def test_discrepancia_humedad():
    """Diferencia de humedad mayor a 10% debe generar discrepancia"""
    actual_mod = {**api_record, "humidity_pct": 65.0}  # diferencia de 15%
    resultado = _detectar_discrepancias(manual_record, actual_mod)
    assert len(resultado) == 1
    assert "Humedad" in resultado[0]


def test_multiples_discrepancias():
    """Varios campos fuera de tolerancia deben generar varias discrepancias"""
    actual_mod = {**api_record, "temperature_c": 28.0, "wind_kph": 40.0}
    resultado = _detectar_discrepancias(manual_record, actual_mod)
    assert len(resultado) == 2  


@patch('backend.core.compare.get_all_records')
@patch('backend.core.compare._get_dato_actual')
def test_comparar_ciudad_sin_registros_manuales(mock_actual, mock_records):
    """Si no hay registros manuales debe devolver None"""
    # Simulamos que el histórico no tiene registros manuales
    mock_records.return_value = {
        "key1": {**manual_record, "source": "WeatherAPI"}  # no es manual
    }
    resultado = comparar_ciudad("Madrid", "centro")
    assert resultado is None


@patch('backend.core.compare.get_all_records')
@patch('backend.core.compare._get_dato_actual')
def test_comparar_ciudad_ok(mock_actual, mock_records):
    """Con registros manuales y API disponible debe devolver el resultado"""
    mock_records.return_value = {"key1": manual_record}
    mock_actual.return_value = api_record

    resultado = comparar_ciudad("Madrid", "centro")

    assert resultado is not None
    assert resultado["city"] == "Madrid"
    assert "historico" in resultado
    assert "actual" in resultado
    assert "discrepancias" in resultado


@patch('backend.core.compare.get_all_records')
@patch('backend.core.compare._get_dato_actual')
def test_comparar_ciudad_api_falla(mock_actual, mock_records):
    """Si la API falla debe devolver None"""
    mock_records.return_value = {"key1": manual_record}
    mock_actual.return_value = None  # la API no responde

    resultado = comparar_ciudad("Madrid", "centro")
    assert resultado is None