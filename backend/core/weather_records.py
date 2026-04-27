from datetime import datetime

def create_weather_record ( 
    record_id: str,
    city: str,
    zone: str,
    temperature_c: float,
    humidity_pct: float,
    wind_kph: float,
    rain_mm: float,
    source: str,
    timestamp: str = None
) -> dict:

    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "record_id": record_id,
        "timestamp": timestamp,
        "zone": zone,
        "city": city,
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "wind_kph": wind_kph,
        "rain_mm": rain_mm,
        "source": source,
    }
