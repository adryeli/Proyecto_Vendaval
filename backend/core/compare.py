import os
from dotenv import load_dotenv
from backend.api.client import fetch_weather_data
from backend.api.normalizer import normalize_weather_data
from backend.storage.json_repo import get_all_records
from backend.utils.logger_config import log_info, log_error

#Definir umbrales de +- valores para ver las discrepancias
TOLERANCIA = {
    "temperature_c": 3.0,    # °C
    "humidity_pct":  10.0,   # %
    "wind_kph":      15.0,   # km/h
}


def _get_dato_actual(city: str, zone: str) -> dict | None:
    
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = os.getenv("API_BASE_URL")

    if not api_key or not base_url:
        log_error("WeatherAPI: Error de configuración -> Revise el .env")
        return None

    raw_data = fetch_weather_data(api_key, base_url, city)

    if raw_data is None:
        return None

    return normalize_weather_data(raw_data, zone)


def _detectar_discrepancias(historico: dict, actual: dict) -> list:
    
    discrepancias = []

    etiquetas = {
        "temperature_c": ("Temperatura", "°C"),
        "humidity_pct":  ("Humedad",     "%"),
        "wind_kph":      ("Viento",      "km/h"),
    }

    for campo, umbral in TOLERANCIA.items():
        val_hist   = historico.get(campo)
        val_actual = actual.get(campo)

        if val_hist is None or val_actual is None:
            continue

        diferencia = abs(float(val_actual) - float(val_hist))
        nombre, unidad = etiquetas[campo]

        if diferencia > umbral:
            discrepancias.append(
                f"{nombre}: histórico {val_hist}{unidad} → "
                f"actual {val_actual}{unidad} ({diferencia:.1f}{unidad})"
            )

    return discrepancias


def comparar_ciudad(city: str, zone: str) -> dict | None:
    
    todos = get_all_records()
    registros_manuales = [
        r for r in todos.values()
        if r.get("city", "").lower() == city.lower()
        and r.get("source", "").lower() == "manual"
    ]

    if not registros_manuales:
        log_error(f"No hay registros manuales para {city}")
        return None

    historico = max(registros_manuales, key=lambda r: r.get("timestamp", ""))

    actual = _get_dato_actual(city, zone)

    if actual is None:
        log_error(f"No se pudo obtener dato actual para {city}")
        return None

    discrepancias = _detectar_discrepancias(historico, actual)
    log_info(f"Comparativa {city}: {len(discrepancias)} discrepancia(s) detectada(s)")

    return {
        "city":          city,
        "zone":          zone,
        "historico":     historico,
        "actual":        actual,
        "discrepancias": discrepancias
    }