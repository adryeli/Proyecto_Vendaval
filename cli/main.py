"""
cli/main.py

Punto de entrada de la interfaz de consola.

Responsabilidades:
- Mostrar la pantalla de bienvenida.
- Gestionar el flujo de autenticación (login / registro).
- Lanzar el menú principal una vez el usuario está autenticado.
"""

# ==============================
# IMPORTACIONES
# ==============================

# Módulos de la capa CLI
from cli.auth import mostrar_pantalla_auth
from cli.menu import show_menu
from cli.display_helpers import mostrar_bienvenida, mostrar_despedida, limpiar_pantalla

# Logging
from backend.utils.logger_config import log_info


# ==============================
# FUNCIÓN DE ENTRADA CLI
# ==============================

def start_cli() -> None:
    """
    Inicia la aplicación de consola.

    Orquesta en orden:
    1. Pantalla de bienvenida.
    2. Flujo de autenticación (login o registro).
    3. Menú principal (solo si el usuario se autenticó).
    4. Pantalla de despedida al salir.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    # ==============================
    # PASO 1 — BIENVENIDA
    # ==============================

    limpiar_pantalla()
    mostrar_bienvenida()

    # ==============================
    # PASO 2 — AUTENTICACIÓN
    # ==============================

    # mostrar_pantalla_auth devuelve el usuario autenticado (dict)
    # o None si el usuario decidió salir sin autenticarse
    usuario = mostrar_pantalla_auth()

    if usuario is None:
        # El usuario eligió salir antes de autenticarse
        mostrar_despedida()
        return

    # ==============================
    # PASO 3 — MENÚ PRINCIPAL
    # ==============================

    log_info(f"Usuario '{usuario['username']}' ha iniciado sesión.")
    limpiar_pantalla()

    # Lanzamos el menú principal pasándole el usuario
    # para que pueda mostrar su nombre y registrar acciones
    show_menu(usuario)

    # ==============================
    # PASO 4 — DESPEDIDA
    # ==============================

    mostrar_despedida()