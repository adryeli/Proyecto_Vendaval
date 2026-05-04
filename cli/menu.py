"""
cli/menu.py

Menú principal y submenús de la aplicación Vendaval.

Responsabilidades:
- Mostrar el menú principal al usuario autenticado.
- Mostrar el último registro de la ciudad preferida del usuario.
- Gestionar la navegación entre submenús.
- Llamar a las funciones del backend en cada opción.
- Validar inputs antes de enviarlos al backend.

IMPORTANTE: Este archivo NO hace lógica de negocio.
Solo recoge datos del usuario, los pasa al backend, y muestra los resultados.
"""

# ==============================
# IMPORTACIONES
# ==============================

import json
import os

from rich.console import Console

# Helpers de la capa CLI
from cli.display_helpers import (
    mostrar_encabezado,
    mostrar_exito,
    mostrar_error,
    mostrar_advertencia,
    mostrar_info,
    mostrar_separador,
    mostrar_tabla_registro,
    mostrar_tabla_historico,
    mostrar_tabla_alertas,
    mostrar_tiempo_actual,
    pedir_confirmacion,
    limpiar_pantalla
)
from cli.input_helpers import (
    pedir_temperatura,
    pedir_humedad,
    pedir_viento,
    pedir_lluvia,
    pedir_fecha,
    pedir_zona
)

# Backend
from backend.api.ingest_weather import ingest_city_weather, ingest_all_zones
from backend.core.alerts import evaluate_alerts
from backend.api.manual_register import manual_weather_record
from backend.storage.json_repo import save_record, get_all_records
from backend.utils.logger_config import log_info, log_warning

console = Console()


# ==============================
# MENÚ PRINCIPAL
# ==============================

def show_menu(usuario: dict) -> None:
    """
    Muestra el menú principal y gestiona la navegación entre opciones.

    Si el usuario tiene ciudad preferida guardada, muestra su último
    registro al entrar. Si no, le pide que elija su zona.

    Parámetros:
        usuario (dict): Diccionario con los datos del usuario autenticado.
            Debe tener al menos la clave 'username'.

    No devuelve ningún valor.
    """
    usuario = _asegurar_zona_usuario(usuario)

    while True:
        limpiar_pantalla()

        # Último registro de la ciudad preferida
        _mostrar_tiempo_zona_usuario(usuario)

        console.print(f"\n[bold cyan]Hola, {usuario['username']}[/bold cyan]  —  ¿Qué quieres hacer?\n")

        console.print("  [bold]1.[/bold] 📝  Registro manual de datos")
        console.print("  [bold]2.[/bold] 🌐  Registro automático de clima")
        console.print("  [bold]3.[/bold] 📊  Consultar histórico")
        console.print("  [bold]4.[/bold] 🚨  Ver alertas del histórico")
        console.print("  [bold]5.[/bold] 🗺   Cambiar mi zona")
        console.print("  [bold]6.[/bold] 🚪  Salir\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        if opcion == "1":
            log_info(f"Usuario '{usuario['username']}' → Registro manual")
            _submenu_registro_manual()

        elif opcion == "2":
            log_info(f"Usuario '{usuario['username']}' → Registro automático de clima")
            _submenu_ingesta_api()

        elif opcion == "3":
            log_info(f"Usuario '{usuario['username']}' → Consultar histórico")
            _submenu_historico()

        elif opcion == "4":
            log_info(f"Usuario '{usuario['username']}' → Ver alertas")
            _submenu_alertas()

        elif opcion == "5":
            log_info(f"Usuario '{usuario['username']}' → Cambiar zona")
            usuario = _cambiar_zona_usuario(usuario)

        elif opcion == "6":
            if pedir_confirmacion("¿Seguro que quieres salir?"):
                log_info(f"Usuario '{usuario['username']}' ha cerrado sesión.")
                break

        else:
            mostrar_error("Opción no válida. Elige un número del 1 al 6.")
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")


# ==============================
# SUBMENÚ 1 — REGISTRO MANUAL
# ==============================

def _submenu_registro_manual() -> None:
    """
    Submenú para registrar un dato climático manualmente.

    Permite revisar el resumen antes de guardar. Si el usuario se equivoca,
    puede repetir el formulario o volver al menú sin guardar.
    """
    while True:
        limpiar_pantalla()
        mostrar_encabezado("📝 Registro manual de datos", "Introduce los datos climáticos paso a paso")
        console.print("[dim]Consejo: en selección de zona puedes escribir 0 para volver.[/dim]")

        fecha = pedir_fecha()

        zona, ciudad = pedir_zona()
        if zona is None:
            mostrar_info("Has vuelto al menú anterior sin guardar datos.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        temperatura = pedir_temperatura()
        humedad = pedir_humedad()
        viento = pedir_viento()
        lluvia = pedir_lluvia()

        registro = manual_weather_record(
            city=ciudad,
            zone=zona,
            temperature_c=temperatura,
            humidity_pct=humedad,
            wind_kph=viento,
            rain_mm=lluvia,
            timestamp=fecha
        )

        if registro is None:
            mostrar_error("El registro manual no es válido.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        limpiar_pantalla()
        mostrar_encabezado("📋 Resumen del registro")
        mostrar_tabla_registro(registro)

        alertas = registro.get("alerts", {}).get("messages", [])
        mostrar_tabla_alertas(alertas)

        console.print("\n[bold cyan]¿Qué quieres hacer con este registro?[/bold cyan]")
        console.print("  [bold]1.[/bold] Guardar registro")
        console.print("  [bold]2.[/bold] Corregir / repetir registro")
        console.print("  [bold]3.[/bold] Volver sin guardar\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        if opcion == "1":
            save_record(registro)
            mostrar_exito("Registro manual guardado correctamente.")
            console.input("\n[dim]Pulsa Enter para volver al menú...[/dim]")
            return

        if opcion == "2":
            mostrar_info("Vamos a repetir el formulario para corregir los datos.")
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
            continue

        if opcion == "3":
            mostrar_info("Registro descartado. Vuelves al menú principal.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        mostrar_error("Opción no válida. No se ha guardado el registro.")
        console.input("\n[dim]Pulsa Enter para volver al menú...[/dim]")
        return


# ==============================
# SUBMENÚ 2 — INGESTA API
# ==============================

def _submenu_ingesta_api() -> None:
    """
    Submenú para obtener datos automáticamente desde WeatherAPI.

    Permite ingestar una ciudad concreta o todas las ciudades configuradas.

    No devuelve ningún valor.
    """
    limpiar_pantalla()
    mostrar_encabezado("🌐 Registro automático de clima", "Obtiene y guarda datos en tiempo real desde WeatherAPI")

    console.print("\n[bold]1.[/bold] Elegir una ciudad")
    console.print("[bold]2.[/bold] Registrar automáticamente todas las ciudades")
    console.print("[bold]3.[/bold] Volver\n")

    opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

    if opcion == "1":
        zona, ciudad = pedir_zona()

        if zona is None:
            mostrar_error("No se pudo cargar la lista de zonas.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        registro = ingest_city_weather(ciudad, zona)

        if registro is None:
            mostrar_error("No se pudieron obtener datos de la API.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        limpiar_pantalla()
        mostrar_encabezado("📡 Datos obtenidos de WeatherAPI")
        mostrar_tabla_registro(registro)

        alertas = registro.get("alerts", {}).get("messages", [])
        mostrar_tabla_alertas(alertas)

        mostrar_exito("Registro guardado correctamente.")

    elif opcion == "2":
        registros = ingest_all_zones()

        if not registros:
            mostrar_error("No se pudo obtener ningún registro.")
            console.input("\n[dim]Pulsa Enter para volver...[/dim]")
            return

        mostrar_exito(f"Ingesta completada. {len(registros)} ciudades procesadas.")

    elif opcion == "3":
        return

    else:
        mostrar_error("Opción no válida.")

    console.input("\n[dim]Pulsa Enter para volver al menú...[/dim]")


# ==============================
# SUBMENÚ 3 — HISTÓRICO
# ==============================

def _submenu_historico() -> None:
    """
    Submenú para consultar el histórico de registros climáticos.

    Permite:
    - Ver todos los registros.
    - Filtrar por zona.
    - Filtrar por fecha.
    - Filtrar por zona y fecha.
    """
    limpiar_pantalla()
    mostrar_encabezado("📊 Histórico de registros")

    while True:
        console.print("\n[bold cyan]¿Cómo quieres consultar el histórico?[/bold cyan]\n")
        console.print("  [bold]1.[/bold] Ver todos los registros")
        console.print("  [bold]2.[/bold] Filtrar por zona")
        console.print("  [bold]3.[/bold] Filtrar por fecha")
        console.print("  [bold]4.[/bold] Filtrar por zona y fecha")
        console.print("  [bold]5.[/bold] Volver al menú principal\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        if opcion == "1":
            registros = get_all_records()

            limpiar_pantalla()
            mostrar_encabezado("📊 Todos los registros")
            mostrar_tabla_historico(registros)

            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "2":
            console.print("\n[bold]Selecciona la zona a filtrar:[/bold]")
            zona_filtro, ciudad_filtro = pedir_zona()

            if zona_filtro is None:
                mostrar_info("Has vuelto al menú anterior.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()

            filtrados = {
                clave: registro
                for clave, registro in todos.items()
                if registro.get("zone") == zona_filtro
            }

            limpiar_pantalla()
            mostrar_encabezado(f"📊 Registros de {ciudad_filtro} ({zona_filtro})")
            mostrar_tabla_historico(filtrados)

            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "3":
            fecha_filtro = console.input(
                "[bold white]Introduce fecha a consultar (YYYY-MM-DD): [/bold white]"
            ).strip()

            todos = get_all_records()

            filtrados = {
                clave: registro
                for clave, registro in todos.items()
                if registro.get("timestamp", "").startswith(fecha_filtro)
            }

            limpiar_pantalla()
            mostrar_encabezado(f"📊 Registros del día {fecha_filtro}")
            mostrar_tabla_historico(filtrados)

            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "4":
            console.print("\n[bold]Selecciona la zona a filtrar:[/bold]")
            zona_filtro, ciudad_filtro = pedir_zona()

            if zona_filtro is None:
                mostrar_info("Has vuelto al menú anterior.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            fecha_filtro = console.input(
                "[bold white]Introduce fecha a consultar (YYYY-MM-DD): [/bold white]"
            ).strip()

            todos = get_all_records()

            filtrados = {
                clave: registro
                for clave, registro in todos.items()
                if registro.get("zone") == zona_filtro
                and registro.get("timestamp", "").startswith(fecha_filtro)
            }

            limpiar_pantalla()
            mostrar_encabezado(
                f"📊 Registros de {ciudad_filtro} ({zona_filtro}) del día {fecha_filtro}"
            )
            mostrar_tabla_historico(filtrados)

            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "5":
            break

        else:
            mostrar_error("Opción no válida. Elige un número del 1 al 5.")

# ==============================
# SUBMENÚ 4 — ALERTAS
# ==============================

def _submenu_alertas() -> None:
    """
    Submenú para ver las alertas activas en el histórico.

    Recorre todos los registros guardados y muestra los que
    tienen alertas activas.

    No devuelve ningún valor.
    """
    limpiar_pantalla()
    mostrar_encabezado("🚨 Panel de alertas", "Registros con alertas activas en el histórico")

    registros = get_all_records()

    if not registros:
        mostrar_advertencia("No hay registros en el histórico todavía.")
        console.input("\n[dim]Pulsa Enter para volver...[/dim]")
        return

    registros_con_alertas = []

    for clave, registro in registros.items():
        mensajes = evaluate_alerts(registro).get("messages", [])
        if mensajes:
            registros_con_alertas.append({
                "registro": registro,
                "alertas": mensajes
            })

    if not registros_con_alertas:
        mostrar_exito("¡Sin alertas! Todos los registros están dentro de los rangos normales.")
    else:
        console.print(f"\n[bold red]Se encontraron {len(registros_con_alertas)} registro(s) con alertas:[/bold red]\n")

        for item in registros_con_alertas:
            r = item["registro"]
            mostrar_separador()
            console.print(
                f"[bold]{r.get('city', '?')}[/bold] "
                f"[dim]({r.get('zone', '?')}) — {r.get('timestamp', '?')}[/dim]"
            )
            mostrar_tabla_alertas(item["alertas"])

    console.input("\n[dim]Pulsa Enter para volver al menú...[/dim]")


# ==============================
# FUNCIONES AUXILIARES INTERNAS
# ==============================

def _mostrar_tiempo_zona_usuario(usuario: dict) -> None:
    """
    Muestra el último registro guardado de la ciudad preferida del usuario.

    Parámetros:
        usuario (dict): El usuario autenticado con city_preferida y zona_preferida.

    No devuelve ningún valor.
    """
    ciudad = usuario.get("city_preferida")
    zona = usuario.get("zona_preferida")

    if not ciudad or not zona:
        return

    registros = get_all_records()

    if not registros:
        mostrar_advertencia("No hay registros guardados todavía.")
        return

    registros_ciudad = [
        r for r in registros.values()
        if r.get("city", "").lower() == ciudad.lower()
    ]

    if not registros_ciudad:
        mostrar_advertencia(f"No hay registros guardados para {ciudad}.")
        return

    ultimo = max(registros_ciudad, key=lambda r: r.get("timestamp", ""))

    alertas = evaluate_alerts(ultimo).get("messages", [])
    mostrar_tiempo_actual(ultimo, alertas)


def _asegurar_zona_usuario(usuario: dict) -> dict:
    """
    Comprueba si el usuario tiene zona preferida y, si no, la pide.

    Parámetros:
        usuario (dict): El usuario autenticado.

    Devuelve:
        dict: El usuario actualizado con zona_preferida y city_preferida.
    """
    if usuario.get("zona_preferida"):
        return usuario

    limpiar_pantalla()
    mostrar_encabezado(
        "🗺  Bienvenida/o a Vendaval",
        "Primera vez que entras — elige tu zona para ver el tiempo"
    )

    console.print(
        "\n[dim]Tu zona preferida aparecerá cada vez que abras la app. "
        "Puedes cambiarla desde el menú principal.[/dim]\n"
    )

    zona, ciudad = pedir_zona()

    if zona is None:
        return usuario

    usuario["zona_preferida"] = zona
    usuario["city_preferida"] = ciudad
    _actualizar_usuario_en_archivo(usuario)

    mostrar_exito(f"Zona guardada: {ciudad} ({zona})")
    console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

    return usuario


def _cambiar_zona_usuario(usuario: dict) -> dict:
    """
    Permite al usuario cambiar su zona preferida.

    Parámetros:
        usuario (dict): El usuario autenticado.

    Devuelve:
        dict: El usuario actualizado con la nueva zona.
    """
    limpiar_pantalla()
    mostrar_encabezado("🗺  Cambiar zona preferida")

    zona_actual = usuario.get("zona_preferida", "ninguna")
    ciudad_actual = usuario.get("city_preferida", "")
    mostrar_info(f"Zona actual: {ciudad_actual} ({zona_actual})")

    console.print("\n[bold]Selecciona tu nueva zona:[/bold]")
    zona, ciudad = pedir_zona()

    if zona is None:
        mostrar_advertencia("No se cambió la zona.")
        return usuario

    usuario["zona_preferida"] = zona
    usuario["city_preferida"] = ciudad
    _actualizar_usuario_en_archivo(usuario)

    mostrar_exito(f"Zona actualizada a: {ciudad} ({zona})")
    console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

    return usuario


def _actualizar_usuario_en_archivo(usuario_actualizado: dict) -> None:
    """
    Actualiza los datos de un usuario en el archivo users.json.

    Parámetros:
        usuario_actualizado (dict): El usuario con los datos ya actualizados.

    No devuelve ningún valor.
    """
    ruta_usuarios = os.path.join(
        os.path.dirname(__file__), "..", "data", "users.json"
    )

    try:
        with open(ruta_usuarios, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = []

    for i, u in enumerate(usuarios):
        if u["username"] == usuario_actualizado["username"]:
            usuarios[i] = usuario_actualizado
            break

    with open(ruta_usuarios, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)