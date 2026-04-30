import json
import random
from datetime import datetime
import os

def load_zones():
    """Lee las zonas y ciudades de config/zones.json."""
    datos_zonas = []
    try:
        with open("config/zones.json", "r", encoding="utf-8") as f:
            parsed_zones = json.load(f)
            if isinstance(parsed_zones, list):
                for z in parsed_zones:
                    zona_val = z.get("zone", "Desconocida")
                    ciudad_val = z.get("city", z.get("ciudad", z.get("name", "Desconocida")))
                    datos_zonas.append({"zone": zona_val, "city": ciudad_val})
            elif isinstance(parsed_zones, dict):
                datos_zonas = [{"zone": k, "city": v} for k, v in parsed_zones.items()]
    except Exception:
        print("⚠️ No se pudo leer config/zones.json. Usando datos de emergencia.")
        datos_zonas = [{"zone": "Centro", "city": "Madrid"}]
    return datos_zonas

def save_json_utf8(data, filename):
    """Guarda los datos en JSON con encoding UTF-8 correcto."""
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ ¡Éxito! Generado {path} con {len(data)} registros.")

def generate_manual_history(datos_zonas):
    """Genera 1 muestra cada 2 años para todas las provincias (Manuales)."""
    records = []
    # Generamos desde 1996 hasta 2026, saltando de 2 en 2 años
    for z in datos_zonas:
        for year in range(1996, 2027, 2):
            # Usamos un mes fijo (ej. Mayo) para los registros manuales
            dt_str = datetime(year, 5, 20, 10, 0).strftime("%Y-%m-%d %H:%M")
            
            records.append({
                "timestamp": dt_str,
                "zone": z["zone"],
                "city": z["city"],
                "temperature_c": round(random.uniform(10.0, 35.0), 1),
                "humidity_pct": round(random.uniform(40.0, 70.0), 1),
                "wind_kph": round(random.uniform(0.0, 25.0), 1),
                "rain_mm": round(random.uniform(0.0, 5.0), 1),
                "source": "Manual"
            })
    save_json_utf8(records, "manual_records.json")

def generate_api_cache(datos_zonas):
    """Genera los datos que ya teníamos para la API (2 muestras al año)."""
    records = []
    for z in datos_zonas:
        for year in range(1996, 2027):
            for month in [1, 7]: 
                if year == 2026 and month > 4: continue
                dt_str = datetime(year, month, 15, 12, 0).strftime("%Y-%m-%d %H:%M")
                records.append({
                    "timestamp": dt_str, "zone": z["zone"], "city": z["city"],
                    "temperature_c": round(random.uniform(-5.0, 45.0), 1),
                    "humidity_pct": round(random.uniform(20.0, 90.0), 1),
                    "wind_kph": round(random.uniform(5.0, 60.0), 1),
                    "rain_mm": round(random.uniform(0.0, 20.0), 1),
                    "source": "API"
                })
    save_json_utf8(records, "weather_cache.json")

if __name__ == "__main__":
    zonas = load_zones()
    generate_api_cache(zonas)     # Genera weather_cache.json
    generate_manual_history(zonas) # Genera manual_records.json