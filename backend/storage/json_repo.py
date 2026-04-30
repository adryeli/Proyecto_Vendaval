"""
Módulo de Persistencia JSON - Proyecto Vendaval (Barlovento Data)

Este archivo contiene las funciones encargadas de gestionar el almacenamiento
físico de los datos climáticos (Estilo Procedural).

Estrategia de Almacenamiento:
Utiliza un diccionario principal donde cada llave es una "clave compuesta" (ej. "2026-04-24 15:30_Madrid").
Esto permite la actualización de JSON sin duplicados.
"""

import json
import os

# Definimos la ruta por defecto como una constante global del módulo
DEFAULT_FILE_PATH = "data/weather_cache.json"

def ensure_file_exists(file_path: str = DEFAULT_FILE_PATH) -> None:
    """
    Comprueba si el archivo JSON y su carpeta contenedora existen.
    Si la carpeta no existe, la crea. Si el archivo no existe, lo inicializa.
    """
    directorio = os.path.dirname(file_path)
    
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)
        
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file)

def save_record(record: dict, file_path: str = DEFAULT_FILE_PATH) -> bool:
    """
    Guarda o actualiza un registro climático en el archivo JSON.
    
    Parámetros:
    record (dict): El dato climático a guardar.
    file_path (str): La ruta del archivo.
    
    Retorna:
    bool: True si se guardó correctamente.
    """
    ensure_file_exists(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Construimos nuestra Clave Compuesta: timestamp + zona
    clave = f"{record['timestamp']}_{record['zone']}"
    
    # Guardamos/Actualizamos el registro
    data[clave] = record
    
    # Sobrescribimos el archivo
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
    return True

def get_all_records(file_path: str = DEFAULT_FILE_PATH) -> dict:
    """
    Lee y devuelve todo el histórico de registros del archivo JSON.
    
    Parámetros:
    file_path (str): La ruta del archivo.
    
    Retorna:
    dict: Diccionario con todos los registros guardados.
    """
    ensure_file_exists(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}