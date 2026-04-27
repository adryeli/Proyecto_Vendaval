"""
Módulo de Persistencia JSON - Proyecto Vendaval (Barlovento Data)

Este archivo contiene la clase JsonRepository, encargada de gestionar el almacenamiento
físico de los datos climáticos obtenidos externa o manualmente.

¿Por qué lo creamos?
Para solucionar la limitación de "datos aislados". El JSON local pasa a ser nuestra 
capa de caché/histórico: guarda lo que ya se obtuvo, permite trabajar sin conexión 
y conserva el acumulado histórico[cite: 27]. Se requiere persistencia en JSON sin pérdida 
ni sobrescritura de datos históricos[cite: 18].

Estrategia de Almacenamiento:
Utiliza un diccionario principal donde cada llave es una "clave compuesta" (ej. "2026-04-24_Madrid").
Esto permite la actualización de JSON sin duplicados[cite: 52]. Si recibimos un dato de la 
misma ciudad en el mismo día, simplemente sobrescribe ese registro específico, manteniendo 
el histórico limpio.
"""

import json
import os

class JsonRepository:
    """
    Repositorio para interactuar con el almacenamiento en formato JSON.
    Centraliza todas las operaciones de lectura y escritura.
    """

    def __init__(self, file_path: str = "data/weather_cache.json"):
        """
        Inicializa el repositorio JSON.
        
        Parámetros:
        file_path (str): La ruta del archivo donde se guardarán los datos.
                         Si Lógica de Negocio no pasa ninguna ruta, por defecto
                         usará 'data/weather_cache.json' para no romper nada.
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        Comprueba si el archivo JSON y su carpeta contenedora existen.
        Si la carpeta no existe, la crea. Si el archivo no existe, lo inicializa.
        """
        # 1. Extraer el nombre de la carpeta de la ruta (ej. 'data' de 'data/weather_cache.json')
        directorio = os.path.dirname(self.file_path)
        
        # 2. Si hay un directorio en la ruta y no existe físicamente, lo creamos
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
            
        # 3. Comprobar si el archivo en sí existe
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump({}, file)

    def save_record(self, record: dict) -> bool:
        """
        Guarda o actualiza un registro climático en el archivo JSON.
        
        Parámetros:
        record (dict): El dato climático a guardar.
        
        Retorna:
        bool: True si se guardó correctamente.
        """
        # 1. Intentamos leer el archivo de forma segura
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo fue borrado o está corrupto/vacío, empezamos de cero
            data = {}
        
        # 2. Construimos nuestra Clave Compuesta
        clave = f"{record['timestamp']}_{record['zone']}"
        
        # 3. Guardamos el registro en el diccionario
        data[clave] = record
        
        # 4. Sobrescribimos el archivo con los datos actualizados
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            
        return True # Avisamos a Application que todo salió perfecto