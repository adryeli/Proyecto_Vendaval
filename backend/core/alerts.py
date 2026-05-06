def check_high_temp_alert(record):
    return record["temperature_c"] >= 40

def check_low_temp_alert(record):
    return record["temperature_c"] <= -8


def check_wind_alert(record):
    return record["wind_kph"] >= 70


def check_low_humidity_info(record):
    return record["humidity_pct"] < 30


def check_high_humidity_info(record):
    return record["humidity_pct"] > 60


def check_heavy_rain_alert(record):
    return 10 < record["rain_mm"] <= 30


def check_heavy_rain_risk_alert(record):
    return record["rain_mm"] > 30


def evaluate_alerts(record):
    messages = []
    results = {}

    high_temp_active = check_high_temp_alert(record)
    results["high_temp_alert"] = high_temp_active
    if high_temp_active:
        messages.append("Alarma: Temperatura muy alta")

    low_temp_active = check_low_temp_alert(record)
    results["low_temp_alert"] = low_temp_active
    if low_temp_active:
        messages.append("Alarma: Temperatura muy baja")

    wind_active = check_wind_alert(record)
    results["wind_alert"] = wind_active
    if wind_active:
        messages.append("Alarma: Riesgo de viento alto")

    low_humidity_active = check_low_humidity_info(record)
    results["low_humidity_info"] = low_humidity_active
    if low_humidity_active:
        messages.append("Información: Humedad ambiental baja")

    high_humidity_active = check_high_humidity_info(record)
    results["high_humidity_info"] = high_humidity_active
    if high_humidity_active:
        messages.append("Información: Humedad ambiental alta")

    heavy_rain_active = check_heavy_rain_alert(record)
    results["heavy_rain_alert"] = heavy_rain_active
    if heavy_rain_active:
        messages.append("Alarma: Lluvia fuerte")

    heavy_rain_risk_active = check_heavy_rain_risk_alert(record)
    results["heavy_rain_risk_alert"] = heavy_rain_risk_active
    if heavy_rain_risk_active:
        messages.append("Alarma: Riesgo de lluvias muy fuertes")

    return {
        "messages": messages,
        "results": results
    }