import pytest
from backend.api.normalizer import normalize_weather_data

@pytest.fixture
def mock_api_data():
    return {
        "location": {"name": "Madrid"},
        "current": {
            "temp_c": 25.5,
            "humidity": 40,
            "wind_kph": 15.0,
            "precip_mm": 0.0,
            "last_updated": "2026-04-29 10:00"
        }
    }

def test_normalize_weather_data_success(mock_api_data):
    result = normalize_weather_data(mock_api_data, zone="Centro")
    assert result is not None
    assert result["city"] == "Madrid"
    assert result["temperature_c"] == 25.5

def test_normalize_weather_data_missing_fields():
    incomplete_data = {
        "location": {}, 
        "current": {"temp_c": 20.0}
    }
    result = normalize_weather_data(incomplete_data, zone="Norte")
    assert result is not None
    assert result["city"] == ""
    assert result["humidity_pct"] == 0.0

def test_normalize_weather_data_invalid_structure():
    invalid_data = {"error": "not found"}
    result = normalize_weather_data(invalid_data, zone="Sur")
    assert result is None