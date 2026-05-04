"""
run.py

Punto de entrada principal del Proyecto Vendaval.

Responsabilidades:
- Configurar el sistema de logging.
- Lanzar la aplicación de consola (CLI).
"""

# ==============================
# IMPORTACIONES
# ==============================

# Configuración de logging del proyecto
from backend.utils.logger_config import setup_logger, log_info, log_error, log_critical

# Punto de entrada de la interfaz de consola
from cli.main import start_cli


# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def main() -> None:
    """
    Función principal del proyecto.

    Inicializa el logging y lanza la interfaz de consola.
    Captura errores inesperados para que el programa no muera de forma fea.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    # Configurar el sistema de logging antes de hacer cualquier otra cosa
    setup_logger()

    log_info("=== PROYECTO VENDAVAL ARRANCADO ===")

    try:
        # Iniciar la aplicación CLI
        start_cli()

    except KeyboardInterrupt:
        # Esto ocurre cuando el usuario pulsa Ctrl+C
        # En lugar de mostrar un error feo, mostramos un mensaje amable
        print("\n\nSaliendo del sistema... ¡Hasta pronto! 🌤")
        log_info("Aplicación cerrada por el usuario (Ctrl+C).")

    except Exception as e:
        # Cualquier otro error inesperado llega aquí
        # Lo registramos en el log y avisamos al usuario
        log_critical(f"Error crítico no controlado: {e}")
        print(f"\n❌ Error inesperado al arrancar: {e}")
        print("Consulta el archivo logs/app.log para más detalles.")


# ==============================
# ARRANQUE DEL PROGRAMA
# ==============================

# Ejecutar solo si este archivo se ejecuta directamente
# Si otro archivo importa run.py, esto NO se ejecuta automáticamente
if __name__ == "__main__":
    main()