import pytest
from backend.core.alerts import (
    evaluate_alerts,
    check_temp_alert,
    check_wind_alert,
    check_high_humidity_alert,
    check_low_humidity_alert,
    check_heavy_rain_alert,
    check_heavy_rain_risk_alert
)

# Record base con valores normales (sin alertas)
normal_record = {
    "temperature_c": 22.0,
    "humidity_pct": 50.0,
    "wind_kph": 20.0,
    "rain_mm": 0.0
}

def test_sin_alertas():
    """Con valores normales no debe haber ninguna alerta"""
    result = evaluate_alerts(normal_record)
    assert result["messages"] == []
    assert result["results"]["temp_alert"] == False
    assert result["results"]["wind_alert"] == False

def test_alerta_temperatura_alta():
    """Temperatura superior a 40°C debe activar la alerta"""
    record = {**normal_record, "temperature_c": 41.0}
    assert check_temp_alert(record) == True

def test_alerta_temperatura_baja():
    """Temperatura inferior a -8°C debe activar la alerta"""
    record = {**normal_record, "temperature_c": -9.0}
    assert check_temp_alert(record) == True

def test_sin_alerta_temperatura():
    """Temperatura dentro del rango no debe activar alerta"""
    record = {**normal_record, "temperature_c": 25.0}
    assert check_temp_alert(record) == False

def test_alerta_viento():
    """Viento igual o superior a 70 km/h debe activar la alerta"""
    record = {**normal_record, "wind_kph": 70.0}
    assert check_wind_alert(record) == True

def test_sin_alerta_viento():
    """Viento inferior a 70 km/h no debe activar alerta"""
    record = {**normal_record, "wind_kph": 69.0}
    assert check_wind_alert(record) == False

def test_alerta_humedad_alta():
    """Humedad superior a 60% debe activar la alerta"""
    record = {**normal_record, "humidity_pct": 61.0}
    assert check_high_humidity_alert(record) == True

def test_alerta_humedad_baja():
    """Humedad inferior a 30% debe activar la alerta"""
    record = {**normal_record, "humidity_pct": 29.0}
    assert check_low_humidity_alert(record) == True

def test_alerta_lluvia_fuerte():
    """Lluvia entre 10 y 30mm debe activar alerta de lluvia fuerte"""
    record = {**normal_record, "rain_mm": 20.0}
    assert check_heavy_rain_alert(record) == True

def test_alerta_lluvia_muy_fuerte():
    """Lluvia superior a 30mm debe activar alerta de riesgo"""
    record = {**normal_record, "rain_mm": 35.0}
    assert check_heavy_rain_risk_alert(record) == True

def test_evaluate_alerts_multiples():
    """Varios campos fuera de rango deben generar varios mensajes"""
    record = {
        "temperature_c": 45.0,
        "humidity_pct": 80.0,
        "wind_kph": 90.0,
        "rain_mm": 0.0
    }
    result = evaluate_alerts(record)
    assert len(result["messages"]) == 3
    assert result["results"]["temp_alert"] == True
    assert result["results"]["wind_alert"] == True
    assert result["results"]["high_humidity_alert"] == True