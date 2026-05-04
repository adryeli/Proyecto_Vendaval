"""
cli/input_helpers.py

Funciones auxiliares para pedir y validar datos al usuario por consola.

Responsabilidades:
- Pedir valores numéricos con validación de rango.
- Pedir y validar fechas.
- Pedir y validar selección de zona/ciudad.
- Pedir texto con longitud mínima.
- Evitar que el programa explote si el usuario escribe algo inesperado.

Cada función es un bucle: el usuario está "atrapado" hasta que da un dato válido.
"""

# ==============================
# IMPORTACIONES
# ==============================

import json
import os
from datetime import datetime
from rich.console import Console

# Importamos las funciones de display para mensajes de error
from cli.display_helpers import mostrar_error, mostrar_advertencia

console = Console()


# ==============================
# INPUTS NUMÉRICOS
# ==============================

def pedir_float(mensaje: str, minimo: float, maximo: float) -> float:
    """
    Pide al usuario un número decimal dentro de un rango permitido.

    El usuario no puede salir del bucle hasta que introduzca un número
    que esté entre minimo y maximo.

    Parámetros:
        mensaje (str): La pregunta o etiqueta que verá el usuario.
        minimo (float): El valor mínimo permitido (inclusive).
        maximo (float): El valor máximo permitido (inclusive).

    Devuelve:
        float: El número validado que introdujo el usuario.
    """
    while True:
        # Pedimos el valor al usuario
        entrada = console.input(
            f"[bold white]{mensaje} [{minimo} - {maximo}]: [/bold white]"
        ).strip()

        # Comprobamos que no esté vacío
        if not entrada:
            mostrar_error("Este campo no puede estar vacío.")
            continue

        # Intentamos convertirlo a número
        # Si el usuario escribió "hola", float() lanzará un error
        # que capturamos con except
        try:
            # Reemplazamos comas por puntos por si el usuario usa coma decimal
            valor = float(entrada.replace(",", "."))
        except ValueError:
            mostrar_error(f"'{entrada}' no es un número válido. Usa solo dígitos (ejemplo: 23.5)")
            continue

        # Comprobamos si está dentro del rango permitido
        if minimo <= valor <= maximo:
            return valor
        else:
            mostrar_error(f"{valor} está fuera del rango permitido ({minimo} a {maximo}).")


def pedir_temperatura() -> float:
    """
    Pide y valida la temperatura en grados Celsius.

    No recibe parámetros.
    Devuelve:
        float: La temperatura validada entre -20 y 50 °C.
    """
    return pedir_float("🌡  Temperatura (°C)", -20.0, 50.0)


def pedir_humedad() -> float:
    """
    Pide y valida el porcentaje de humedad.

    No recibe parámetros.
    Devuelve:
        float: La humedad validada entre 0 y 100 %.
    """
    return pedir_float("💧 Humedad (%)", 0.0, 100.0)


def pedir_viento() -> float:
    """
    Pide y valida la velocidad del viento en km/h.

    No recibe parámetros.
    Devuelve:
        float: La velocidad del viento validada entre 0 y 200 km/h.
    """
    return pedir_float("💨 Viento (km/h)", 0.0, 200.0)


def pedir_lluvia() -> float:
    """
    Pide y valida la cantidad de lluvia en milímetros.

    No recibe parámetros.
    Devuelve:
        float: La lluvia validada entre 0 y 500 mm.
    """
    return pedir_float("🌧  Lluvia (mm)", 0.0, 500.0)


# ==============================
# INPUTS DE FECHA
# ==============================

def pedir_fecha() -> str:
    """
    Pide al usuario una fecha y hora en formato YYYY-MM-DD HH:MM.

    Si el usuario pulsa Enter, usa la fecha y hora actual.

    Valida que:
    - El formato sea correcto.
    - La fecha/hora no sea futura.

    Devuelve:
        str: Fecha y hora validada en formato 'YYYY-MM-DD HH:MM'.
    """
    while True:
        entrada = console.input(
            "[bold white]📅 Fecha y hora (YYYY-MM-DD HH:MM): [/bold white]"
        ).strip()

        # Si el usuario pulsa Enter, usamos fecha y hora actual
        if not entrada:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
            console.print(f"[dim]Usando fecha y hora actual: {ahora}[/dim]")
            return ahora

        # Intentamos interpretar fecha y hora
        try:
            fecha_hora = datetime.strptime(entrada, "%Y-%m-%d %H:%M")
        except ValueError:
            mostrar_error(
                f"'{entrada}' no tiene el formato correcto. Usa YYYY-MM-DD HH:MM "
                "(ejemplo: 2026-05-04 18:30)"
            )
            continue

        # Comprobamos que no sea una fecha futura
        if fecha_hora > datetime.now():
            mostrar_error("No puedes registrar datos de fechas futuras.")
            continue

        return entrada


# ==============================
# SELECCIÓN DE ZONA / CIUDAD
# ==============================

def pedir_zona() -> tuple:
    """
    Muestra un menú numerado con las zonas disponibles en config/zones.json
    y devuelve la zona y ciudad elegidas por el usuario.

    No recibe parámetros.
    Devuelve:
        tuple: (zone, city) — la zona y ciudad seleccionadas.
               Devuelve (None, None) si no se puede cargar la configuración.
    """
    # ==============================
    # CARGAMOS LAS ZONAS DEL JSON
    # ==============================

    # Buscamos el archivo zones.json relativo a la raíz del proyecto
    ruta_zones = os.path.join(
        os.path.dirname(__file__), "..", "config", "zones.json"
    )

    try:
        with open(ruta_zones, "r", encoding="utf-8") as f:
            zonas = json.load(f)
    except FileNotFoundError:
        mostrar_error("No se encontró el archivo config/zones.json.")
        return None, None
    except json.JSONDecodeError:
        mostrar_error("El archivo config/zones.json está corrupto.")
        return None, None

    # ==============================
    # MOSTRAMOS EL MENÚ DE ZONAS
    # ==============================

    console.print("\n[bold cyan]🗺  Zonas disponibles:[/bold cyan]")

    for i, zona in enumerate(zonas, start=1):
        console.print(f"  [dim]{i:2}.[/dim] {zona['city']} [dim]({zona['zone']})[/dim]")

    # ==============================
    # PEDIMOS LA SELECCIÓN
    # ==============================

    while True:
        entrada = console.input(
            f"\n[bold white]Selecciona una zona (1-{len(zonas)}) o 0 para volver: [/bold white]"
        ).strip()

        # Permitimos volver al menú anterior sin romper el programa.
        if entrada == "0":
            return None, None

        try:
            indice = int(entrada) - 1  # Restamos 1 porque las listas empiezan en 0
        except ValueError:
            mostrar_error(f"Escribe un número entre 1 y {len(zonas)}, o 0 para volver.")
            continue

        if 0 <= indice < len(zonas):
            zona_elegida = zonas[indice]
            return zona_elegida["zone"], zona_elegida["city"]
        else:
            mostrar_error(f"Número fuera de rango. Elige entre 1 y {len(zonas)}.")


# ==============================
# INPUTS DE TEXTO
# ==============================

def pedir_texto(mensaje: str, longitud_min: int = 1) -> str:
    """
    Pide al usuario un texto con longitud mínima.

    Parámetros:
        mensaje (str): La pregunta o etiqueta que verá el usuario.
        longitud_min (int): Número mínimo de caracteres requeridos. Por defecto 1.

    Devuelve:
        str: El texto validado introducido por el usuario.
    """
    while True:
        entrada = console.input(f"[bold white]{mensaje}: [/bold white]").strip()

        if len(entrada) >= longitud_min:
            return entrada
        else:
            mostrar_error(
                f"Este campo requiere al menos {longitud_min} carácter(es). "
                f"Has introducido {len(entrada)}."
            )


def pedir_contrasena(mensaje: str = "🔑 Contraseña") -> str:
    """
    Pide una contraseña al usuario (oculta los caracteres con asteriscos).

    Parámetros:
        mensaje (str): La etiqueta del campo de contraseña.

    Devuelve:
        str: La contraseña introducida por el usuario (sin procesar).
    """
    # Rich tiene soporte nativo para passwords — oculta los caracteres
    return console.input(f"[bold white]{mensaje}: [/bold white]", password=True)


# ==============================
# SELECCIÓN DE OPCIÓN DE MENÚ
# ==============================

def pedir_opcion_menu(opciones_validas: list) -> str:
    """
    Pide al usuario que elija entre un conjunto de opciones válidas.

    Parámetros:
        opciones_validas (list): Lista de strings con las opciones aceptadas.
            Ejemplo: ["1", "2", "3", "s", "n"]

    Devuelve:
        str: La opción elegida, ya validada.
    """
    while True:
        entrada = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip().lower()

        if entrada in opciones_validas:
            return entrada
        else:
            mostrar_error(f"'{entrada}' no es una opción válida. Prueba con: {', '.join(opciones_validas)}")