import os
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from backend.api.ingest_weather import ingest_all_zones, ingest_city_weather
from backend.storage.json_repo import get_all_records
from backend.utils.logger_config import log_info, log_error

#Ruta zonas configuradas
ZONE_FILE_PATH = "config/zones.json"

def _get_zone_for_city(city: str) -> str | None:
    try:
        with open(ZONE_FILE_PATH, "r") as f:
            zones = json.load(f)
        for z in zones:
            if z.get("city", "").lower() == city.lower():
                return z.get("zone")
        return None
    except Exception as e:
        log_error(f"Error al leer {ZONE_FILE_PATH}: {e}")
        return None 

def start_schedule_all(SCHEDULER_INTERVAL_MINUTES) -> None:
    #Creamos el scheduler de forma blocking, es decir que bloquea la ejecución hasta que se detenga.
    scheduler = BlockingScheduler()

    #Añadimos el job al scheduler cada X minutos.
    scheduler.add_job(
        ingest_all_zones,
        trigger="interval",
        minutes=SCHEDULER_INTERVAL_MINUTES
    )
    log_info(f"PScheduler activado: Cada {SCHEDULER_INTERVAL_MINUTES} minutos se registrará el clima de todas las zonas")
    log_info("Presiona Ctrl+C para detener el programador.")
    
    try:
        ingest_all_zones()
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log_info("Scheduler ha sido detenido por el usuario")
    except Exception as e:
        log_error(f"Error en el scheduler: {e}")
        scheduler.shutdown()

def start_schedule_city(city: str, SCHEDULER_INTERVAL_MINUTES: int):
    zone = _get_zone_for_city(city)
    if zone is None:
        log_error(f"Ciudad '{city}' no encontrada en zones.json. Scheduler no iniciado.")
        return
    
    scheduler = BlockingScheduler()
    
    #Diferencia con el anterior: pasamos argumentos a la funcion ingest_city_weather
    scheduler.add_job(
        ingest_city_weather,
        trigger="interval",
        minutes=SCHEDULER_INTERVAL_MINUTES,
        args=[city, zone]
    )
    
    log_info(f"Scheduler activado: Cada {SCHEDULER_INTERVAL_MINUTES} minutos se registrará el clima de {city}")
    log_info("Presiona Ctrl+C para detener el programador.")
    
    try:
        ingest_city_weather(city, zone)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log_info("Scheduler ha sido detenido por el usuario")
    except Exception as e:
        log_error(f"Error en el scheduler: {e}")
        scheduler.shutdown()
