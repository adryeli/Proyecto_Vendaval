from datetime import datetime


def create_weather_record ( 
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "timestamp": timestamp,
        "zone": zone,
        "city": city,
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "wind_kph": wind_kph,
        "rain_mm": rain_mm,
        "source": source,
    }
