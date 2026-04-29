"""
cli/main.py

Punto de entrada de la interfaz de consola.
Solo orquesta el menú.
"""

from cli.menu import show_menu


def start_cli() -> None:
    """
    Inicia la aplicación de consola.
    """
    print("🌪 Bienvenida/o a Proyecto Vendaval")
    show_menu()