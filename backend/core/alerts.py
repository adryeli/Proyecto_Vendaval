def check_temp_alert(record):
    return record["temperature_c"] < -8 or record["temperature_c"] > 40


def check_wind_alert(record):
    return record["wind_kph"] >= 70


def check_humidity_alert(record):
    return (0 < record["humidity_pct"] <= 20) or (70 < record["humidity_pct"] <= 100)


def check_heavy_rain_alert(record):
    return 10 < record["rain_mm"] <= 30


def check_heavy_rain_risk_alert(record):
    return record["rain_mm"] > 30


def evaluate_alerts(record):
    messages = []
    results = {}

    temp_active = check_temp_alert(record)
    results["temp_alert"] = temp_active
    if temp_active:
        messages.append("Alarma: Riesgo de temperatura")

    wind_active = check_wind_alert(record)
    results["wind_alert"] = wind_active
    if wind_active:
        messages.append("Alarma: Riesgo de viento alto")

    humidity_active = check_humidity_alert(record)
    results["humidity_alert"] = humidity_active
    if humidity_active:
        messages.append("Alarma: Riesgo de humedad")

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