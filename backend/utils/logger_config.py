import logging 
import os


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger():

    """
    Configura el sistema de logging para que escriba en un archivo y
    opcionalmente en la consola.
    """

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )
    
def log_info(message):
    """Eventos normales: inicio de app, navegación por menús."""
    logging.info(message)
    
   
def log_warning(message):
    """Alertas: duplicados detectados, valores en el límite de rango.""" 
    logging.warning(message)


def log_error(message):
    """Errores: fallos al leer/escribir archivos, errores de conversión."""
    logging.error(message)


def log_critical(message):
    """Fallos graves: la aplicación no puede continuar."""
    logging.critical(message)
