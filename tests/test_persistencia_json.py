import pytest
import os
from backend.storage.json_repo import save_record, get_all_records

@pytest.fixture
def tmp_json(tmp_path):
    # pytest crea una carpeta temporal y la borra automáticamente al acabar
    return str(tmp_path / "test_cache.json")

def test_save_and_retrieve_record(tmp_json):
    # 1. Preparamos el dato de prueba
    dato = {
        "timestamp": "2026-04-29 16:00",
        "zone": "Barcelona",
        "temperature_c": 18.0,
        "humidity_pct": 65.0
    }

    # 2. Ejecutamos tus funciones
    save_record(dato, file_path=tmp_json)
    historial = get_all_records(file_path=tmp_json)

    # 3. Comprobamos (asserts) adaptados a tu estructura de diccionarios
    assert len(historial) == 1
    
    # Construimos la clave que tu función save_record debería haber creado
    clave_esperada = "2026-04-29 16:00_Barcelona"
    
    # Afirmamos que esa clave existe en el historial
    assert clave_esperada in historial
    # Afirmamos que los datos dentro de esa clave son correctos
    assert historial[clave_esperada]["zone"] == "Barcelona"
    assert historial[clave_esperada]["temperature_c"] == 18.0

def test_multiple_records_accumulate(tmp_json):
    # Añadimos los 'timestamp' obligatorios para que tu clave compuesta funcione bien
    save_record({"timestamp": "2026-04-29 10:00", "zone": "Madrid"}, file_path=tmp_json)
    save_record({"timestamp": "2026-04-29 11:00", "zone": "Valencia"}, file_path=tmp_json)

    historial = get_all_records(file_path=tmp_json)
    assert len(historial) == 2

def test_get_all_records_empty_file(tmp_json):
    historial = get_all_records(file_path=tmp_json)
    # Tu función devuelve un diccionario vacío si no hay archivo, no una lista vacía
    assert historial == {}

def test_save_to_different_files(tmp_path):
    # 1. Pytest nos da una carpeta temporal, y nosotros creamos dos rutas distintas dentro
    archivo_api = str(tmp_path / "weather_cache.json")
    archivo_manual = str(tmp_path / "manual_records.json")

    # 2. Preparamos dos datos simulados distintos
    dato_api = {"timestamp": "2026-04-30 10:00", "zone": "Madrid", "source": "API"}
    dato_manual = {"timestamp": "2026-04-30 10:05", "zone": "Madrid", "source": "Manual"}

    # 3. Guardamos cada dato apuntando a su archivo correspondiente con tu misma función
    save_record(dato_api, file_path=archivo_api)
    save_record(dato_manual, file_path=archivo_manual)

    # 4. Leemos los historiales por separado
    historial_api = get_all_records(file_path=archivo_api)
    historial_manual = get_all_records(file_path=archivo_manual)

    # 5. Comprobamos que no se han mezclado
    assert len(historial_api) == 1
    assert len(historial_manual) == 1
    
    # Comprobamos que el origen de los datos es el correcto en cada archivo
    assert historial_api["2026-04-30 10:00_Madrid"]["source"] == "API"
    assert historial_manual["2026-04-30 10:05_Madrid"]["source"] == "Manual"