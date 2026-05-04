import pytest
from backend.core.weather_records import create_weather_record
from backend.core.validator import validate_record

#comprobamos estructura + datos correctos

def test_create_weather_record_basic():
    record_try = create_weather_record(
        city="Madrid",
        zone="Centro",
        temperature_c=25.5,
        humidity_pct=40,
        wind_kph=10,
        rain_mm=0,
        source="manual"
    )

    assert isinstance(record_try, dict)

    assert record_try["city"] == "Madrid"
    assert record_try["zone"] == "Centro"
    assert record_try["temperature_c"] == 25.5
    assert record_try["humidity_pct"] == 40
    assert record_try["wind_kph"] == 10
    assert record_try["rain_mm"] == 0
    assert record_try["source"] == "manual"

    assert "timestamp" in record_try
    assert record_try["timestamp"] is not None
    assert isinstance(record_try["timestamp"], str)

#comprobamos que no se rompe el esquema básico

def test_weather_record_schema_keys():
    record_try = create_weather_record(
        city="Madrid",
        zone="Centro",
        temperature_c=20,
        humidity_pct=50,
        wind_kph=5,
        rain_mm=1,
        source="api"
    )

    expected_keys = {
        "timestamp",
        "zone",
        "city",
        "temperature_c",
        "humidity_pct",
        "wind_kph",
        "rain_mm",
        "source"
    }

    assert set(record_try.keys()) == expected_keys

#comprobamos si detecta errores de campo
# sin error, positivo

def test_create_and_validate_weather_record_success():
    record_try = create_weather_record(
        city="Madrid",
        zone="Centro",
        temperature_c=25.0,
        humidity_pct=45.0,
        wind_kph=12.0,
        rain_mm=0.0,
        source="manual"
    )

    is_valid, message = validate_record(record_try)

    assert is_valid is True
    assert message == "Record is valid"

# con error, negativo

def test_create_and_validate_weather_record_invalid_temperature():
    record_try = create_weather_record(
        city="Madrid",
        zone="Centro",
        temperature_c="HOT",  # ❌ tipo incorrecto
        humidity_pct=45.0,
        wind_kph=12.0,
        rain_mm=0.0,
        source="manual"
    )

    is_valid, message = validate_record(record_try)

    assert is_valid is False
    assert message == "temperature_c must be number"

#comprobamos rangos

def test_validate_weather_record_out_of_range():
    record_try = create_weather_record(
        city="Madrid",
        zone="Centro",
        temperature_c=-200.0,  #fuera de rango lógico
        humidity_pct=50.0,
        wind_kph=10.0,
        rain_mm=0.0,
        source="api"
    )

    is_valid, message = validate_record(record_try)

    assert is_valid is False
    assert message == "temperature out of range"