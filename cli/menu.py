"""
cli/menu.py

Muestra el menú principal y gestiona la navegación básica.
"""

def show_menu() -> None:
    """
    Muestra el menú principal del sistema.
    """
    while True:
        print("\n🌪 --- PROYECTO VENDAVAL ---")
        print("1. Registrar dato manual")
        print("2. Ingesta automática (WeatherAPI)")
        print("3. Consultar histórico")
        print("4. Comparar manual vs API")
        print("5. Iniciar scheduler")
        print("6. Salir")

        option = input("Selecciona una opción: ")

        if option == "1":
            print("Funcionalidad manual en construcción 🚧")

        elif option == "2":
            print("Ingesta API en construcción 🚧")

        elif option == "3":
            print("Consulta histórico en construcción 🚧")

        elif option == "4":
            print("Comparativa en construcción 🚧")

        elif option == "5":
            print("Scheduler en construcción 🚧")

        elif option == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")