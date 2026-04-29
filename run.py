"""
run.py

Punto de entrada principal del Proyecto Vendaval.

Responsabilidades:
- Configurar el sistema de logging.
- Lanzar la aplicación de consola (CLI).
"""

# Configuración de logging del proyecto
from backend.utils.logger_config import setup_logger

# Punto de entrada de la interfaz de consola
from cli.main import start_cli


def main() -> None:
    """
    Función principal del proyecto.

    Inicializa el logging y lanza la interfaz de consola.
    """
    # Configurar logging global del sistema
    setup_logger()

    # Iniciar la aplicación CLI
    start_cli()


# Ejecutar solo si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()