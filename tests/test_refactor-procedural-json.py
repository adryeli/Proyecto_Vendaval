from backend.storage.json_repo import save_record, get_all_records

# Definimos una ruta que todos puedan ver en la carpeta data
RUTA_DEMO = "data/demo_cache.json"

print("--- INICIANDO DEMOSTRACIÓN VISUAL DE PERSISTENCIA ---")

# 1. Creamos un dato falso (simulando la API o la entrada manual)
dato_prueba = {
    "timestamp": "2026-04-29 16:00",
    "zone": "Barcelona",
    "temperature_c": 18.0,
    "humidity_pct": 65.0
}

# 2. Lo guardamos en el archivo visible
print(f"1. Guardando dato de prueba en: {RUTA_DEMO}...")
save_record(dato_prueba, file_path=RUTA_DEMO)
print("¡Dato guardado con éxito!\n")

# 3. Lo leemos usando nuestra función procedural
print("2. Leyendo el historial completo desde el archivo...")
historial = get_all_records(file_path=RUTA_DEMO)

# 4. Lo mostramos por consola para que los compañeros lo vean
print("¡Lectura exitosa! Esto es lo que hay dentro del archivo:")
print(historial)
print("\n--- FIN DE LA DEMOSTRACIÓN ---")
print("Nota para el equipo: Podéis abrir el archivo 'data/demo_cache.json' para ver que realmente se ha creado el fichero físico. ¡Acordaos de borrarlo cuando terminéis de mirar!")