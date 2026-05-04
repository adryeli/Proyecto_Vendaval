from backend.core.weather_records import create_weather_record
from backend.core.validator import validate_record
from backend.core.alerts import evaluate_alerts
from backend.utils.logger_config import log_error, log_info


def manual_weather_record(
    city,
    zone,
    temperature_c,
    humidity_pct,
    wind_kph,
    rain_mm,
    timestamp
):
    record = create_weather_record(
        city=city,
        zone=zone,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        wind_kph=wind_kph,
        rain_mm=rain_mm,
        source="Manual",
        timestamp=timestamp
    )

    is_valid, message = validate_record(record)

    if not is_valid:
        log_error(f"Registro manual inválido para {city}: {message}")
        return None

    alerts = evaluate_alerts(record)

    final_record = {
        **record,
        "alerts": alerts
    }

    log_info(f"Registro manual preparado para {city} ({zone})")

    return final_record