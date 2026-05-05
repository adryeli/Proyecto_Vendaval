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
    mostrar_comparativa,
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
from backend.core.compare import comparar_ciudad
from backend.scheduler.scheduler import start_schedule_all, start_schedule_city 
from backend.stats.cyber_dashboard import run_dashboard

console = Console()


# ==============================
# MENÚ PRINCIPAL
# ==============================

def show_menu(usuario: dict) -> None:
    """
    Muestra el menú principal y gestiona la navegación entre opciones.

    Parámetros:
        usuario (dict): Diccionario con los datos del usuario autenticado.

    No devuelve ningún valor.
    """
    #Es una función de normalización / seguridad del dato.
    usuario = _asegurar_zona_usuario(usuario) 

    while True:
        limpiar_pantalla()

        # Último registro de la ciudad preferida
        _mostrar_tiempo_zona_usuario(usuario)

        console.print(f"\n[bold cyan]Hola, {usuario['username']}[/bold cyan]  —  ¿Qué quieres hacer?\n")

        console.print("  [bold]1.[/bold] 📝  Registro manual de datos")
        console.print("  [bold]2.[/bold] 🌐  Registro automático de clima")
        console.print("  [bold]3.[/bold] 📊  Consultar histórico")
        console.print("  [bold]4.[/bold] 🚨  Historial de alertas")
        console.print("  [bold]5.[/bold] 📈  Mostrar estadísticas registradas")
        console.print("  [bold]6.[/bold] 🗺   Consultar información de una zona")
        console.print("  [bold]7.[/bold] Comparar manual vs dato API")
        console.print("  [bold]8.[/bold] Scheduler (Iniciar/Detener)")
        console.print("  [bold]9.[/bold] 🚪  Salir\n")

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
            log_info(f"Usuario '{usuario['username']}' → Historial de alertas")
            _submenu_historial_alertas()

        elif opcion == "5":
            log_info(f"Usuario '{usuario['username']}' → Estadísticas")
            _submenu_estadisticas()

        elif opcion == "6":
            log_info(f"Usuario '{usuario['username']}' → Cambiar zona")
            usuario = _cambiar_zona_usuario(usuario)

        elif opcion == "7":
            limpiar_pantalla()
            mostrar_encabezado("Comparativa histórico manual vs actual", "Selecciona una ciudad")

            zona, ciudad = pedir_zona()

            if zona is None:
                continue

            console.print(f"\n[dim]Obteniendo dato actual de {ciudad}...[/dim]")
            resultado = comparar_ciudad(ciudad, zona)

            if resultado is None:
                mostrar_error("No se pudo completar la comparativa.")
            else:
                limpiar_pantalla()
                mostrar_encabezado(f"Comparativa Manual vs API — {ciudad}")
                mostrar_comparativa(resultado)

            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
    
        elif opcion == "8":
            limpiar_pantalla()
            mostrar_encabezado("Scheduler automático", "Ingesta periódica sin intervención del usuario")

            console.print("\n[bold]1.[/bold] Todas las zonas")
            console.print("[bold]2.[/bold] Una ciudad concreta")
            console.print("[bold]3.[/bold] Volver\n")

            sub = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

            if sub == "1":
                entrada = console.input("[bold yellow]▶  Minutos entre ingesta (Enter = 60): [/bold yellow]").strip()
                minutos = int(entrada) if entrada.isdigit() else 60
                mostrar_info(f"Iniciando scheduler para todas las zonas cada {minutos} min. Ctrl+C para detener.")
                start_schedule_all(minutos)
                mostrar_info("Scheduler detenido. Volviendo al menú.")

            elif sub == "2":
                zona, ciudad = pedir_zona()
                if ciudad is None:
                    continue
                entrada = console.input("[bold yellow]▶  Minutos entre ingesta (Enter = 60): [/bold yellow]").strip()
                minutos = int(entrada) if entrada.isdigit() else 60
                mostrar_info(f"Iniciando scheduler para {ciudad} cada {minutos} min. Ctrl+C para detener.")
                start_schedule_city(ciudad, minutos)
                mostrar_info("Scheduler detenido. Volviendo al menú.")

            elif sub == "3":
                continue
            else:
                mostrar_error("Opción no válida.")

        elif opcion == "9":
                if pedir_confirmacion("¿Seguro que quieres salir?"):
                    log_info(f"Usuario '{usuario['username']}' ha cerrado sesión.")
                    break
        
        else:
            mostrar_error("Opción no válida. Elige un número del 1 al 8.")
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
        console.print("[dim]Consejo: Pule Enter para que se introduzca automáticamente la fecha y hora actual.[/dim]")

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

    Permite filtrar por:
    - Ciudad (referida como zona en la interfaz)
    - Fecha
    - Ciudad y fecha combinadas
    - O ver todos los registros sin filtro

    CAMBIO: el filtro por zona ahora filtra por CIUDAD concreta,
    no por zona geográfica. Así se puede ver p.ej. solo Madrid o solo Bilbao.
    """
    while True:
        limpiar_pantalla()
        mostrar_encabezado("📊 Histórico de registros")

        console.print("\n[bold cyan]¿Cómo quieres consultar el histórico?[/bold cyan]\n")
        console.print("  [bold]1.[/bold] Ver todos los registros")
        console.print("  [bold]2.[/bold] Filtrar por ciudad")
        console.print("  [bold]3.[/bold] Filtrar por fecha")
        console.print("  [bold]4.[/bold] Filtrar por ciudad y fecha")
        console.print("  [bold]5.[/bold] Volver al menú principal\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        if opcion == "1":
            # ==============================
            # TODOS LOS REGISTROS
            # ==============================
            registros = get_all_records()
            limpiar_pantalla()
            mostrar_encabezado("📊 Todos los registros")
            mostrar_tabla_historico(registros)
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "2":
            # ==============================
            # FILTRAR POR CIUDAD
            # ==============================

            # pedir_zona() devuelve (zona, ciudad) — usamos ciudad para filtrar
            # así el usuario elige de la lista y no tiene que escribir a mano
            console.print("\n[bold]Selecciona la ciudad:[/bold]")
            _, ciudad_filtro = pedir_zona()

            if ciudad_filtro is None:
                mostrar_info("Has vuelto al menú anterior.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()

            # Filtramos comparando city en minúsculas para evitar problemas de mayúsculas
            filtrados = {
                clave: registro
                for clave, registro in todos.items()
                if registro.get("city", "").lower() == ciudad_filtro.lower()
            }

            limpiar_pantalla()
            mostrar_encabezado(f"📊 Registros de {ciudad_filtro}")
            mostrar_tabla_historico(filtrados)
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "3":
            # ==============================
            # FILTRAR POR FECHA
            # ==============================

            # Pedimos la fecha — el usuario puede escribir solo YYYY-MM-DD
            # y se buscarán todos los registros de ese día (independiente de la hora)
            fecha_filtro = console.input(
                "[bold white]📅 Introduce fecha (YYYY-MM-DD): [/bold white]"
            ).strip()

            if not fecha_filtro:
                mostrar_error("La fecha no puede estar vacía.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()

            # startswith() permite buscar por día completo aunque el timestamp
            # incluya horas y minutos (ej: "2026-05-04 18:30" empieza por "2026-05-04")
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
            # ==============================
            # FILTRAR POR CIUDAD Y FECHA
            # ==============================

            console.print("\n[bold]Selecciona la ciudad:[/bold]")
            _, ciudad_filtro = pedir_zona()

            if ciudad_filtro is None:
                mostrar_info("Has vuelto al menú anterior.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            fecha_filtro = console.input(
                "[bold white]📅 Introduce fecha (YYYY-MM-DD): [/bold white]"
            ).strip()

            if not fecha_filtro:
                mostrar_error("La fecha no puede estar vacía.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()

            # Aplicamos los dos filtros a la vez con 'and'
            filtrados = {
                clave: registro
                for clave, registro in todos.items()
                if registro.get("city", "").lower() == ciudad_filtro.lower()
                and registro.get("timestamp", "").startswith(fecha_filtro)
            }

            limpiar_pantalla()
            mostrar_encabezado(f"📊 Registros de {ciudad_filtro} — {fecha_filtro}")
            mostrar_tabla_historico(filtrados)
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "5":
            break

        else:
            mostrar_error("Opción no válida. Elige un número del 1 al 5.")


# ==============================
# SUBMENÚ 4 — HISTORIAL DE ALERTAS
# ==============================

def _submenu_historial_alertas() -> None:
    """
    Submenú para consultar el historial de alertas.

    Permite filtrar las alertas por:
    - Ver todas las alertas del histórico
    - Filtrar alertas por ciudad
    - Filtrar alertas por fecha
    - Filtrar alertas por ciudad y fecha

    Solo muestra registros que tienen al menos una alerta activa.
    """
    while True:
        limpiar_pantalla()
        mostrar_encabezado("🚨 Historial de alertas", "Registros con alertas activas")

        console.print("\n[bold cyan]¿Cómo quieres consultar las alertas?[/bold cyan]\n")
        console.print("  [bold]1.[/bold] Ver todas las alertas")
        console.print("  [bold]2.[/bold] Filtrar alertas por ciudad")
        console.print("  [bold]3.[/bold] Filtrar alertas por fecha")
        console.print("  [bold]4.[/bold] Filtrar alertas por ciudad y fecha")
        console.print("  [bold]5.[/bold] Volver al menú principal\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        if opcion == "1":
            # Todos los registros → filtramos los que tienen alertas
            todos = get_all_records()
            _mostrar_alertas_de_registros(todos, "Todas las alertas del histórico")

        elif opcion == "2":
            # Filtramos primero por ciudad, luego mostramos alertas de esos registros
            console.print("\n[bold]Selecciona la ciudad:[/bold]")
            _, ciudad_filtro = pedir_zona()

            if ciudad_filtro is None:
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()
            filtrados = {
                k: v for k, v in todos.items()
                if v.get("city", "").lower() == ciudad_filtro.lower()
            }
            _mostrar_alertas_de_registros(filtrados, f"Alertas de {ciudad_filtro}")

        elif opcion == "3":
            # Filtramos por fecha y mostramos alertas de esos registros
            fecha_filtro = console.input(
                "[bold white]📅 Introduce fecha (YYYY-MM-DD): [/bold white]"
            ).strip()

            if not fecha_filtro:
                mostrar_error("La fecha no puede estar vacía.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()
            filtrados = {
                k: v for k, v in todos.items()
                if v.get("timestamp", "").startswith(fecha_filtro)
            }
            _mostrar_alertas_de_registros(filtrados, f"Alertas del día {fecha_filtro}")

        elif opcion == "4":
            # Filtramos por ciudad Y fecha
            console.print("\n[bold]Selecciona la ciudad:[/bold]")
            _, ciudad_filtro = pedir_zona()

            if ciudad_filtro is None:
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            fecha_filtro = console.input(
                "[bold white]📅 Introduce fecha (YYYY-MM-DD): [/bold white]"
            ).strip()

            if not fecha_filtro:
                mostrar_error("La fecha no puede estar vacía.")
                console.input("\n[dim]Pulsa Enter para continuar...[/dim]")
                continue

            todos = get_all_records()
            filtrados = {
                k: v for k, v in todos.items()
                if v.get("city", "").lower() == ciudad_filtro.lower()
                and v.get("timestamp", "").startswith(fecha_filtro)
            }
            _mostrar_alertas_de_registros(
                filtrados, f"Alertas de {ciudad_filtro} — {fecha_filtro}"
            )

        elif opcion == "5":
            break

        else:
            mostrar_error("Opción no válida. Elige un número del 1 al 5.")


# ==============================
# SUBMENÚ 5 — ESTADÍSTICAS (EN CONSTRUCCIÓN)
# ==============================

def _submenu_estadisticas() -> None:
    """
    Abre el dashboard interactivo de estadísticas.

    La ventana de Matplotlib se abre en primer plano.
    Al cerrarla (o si falla), se regresa al menú principal.
    """
    limpiar_pantalla()
    mostrar_encabezado("📈  Dashboard de estadísticas")
    console.print("[dim]Abriendo el panel de visualización...[/dim]\n")
    console.print("[dim]Cierra la ventana gráfica para volver al menú.[/dim]\n")

    try:
        run_dashboard()
    except Exception as e:
        log_warning(f"Error al abrir el dashboard: {e}")
        mostrar_error(f"No se pudo abrir el dashboard: {e}")
    finally:
        console.input("\n[dim]Pulsa Enter para volver al menú...[/dim]")


# ==============================
# FUNCIONES AUXILIARES INTERNAS
# ==============================

def _mostrar_alertas_de_registros(registros: dict, titulo: str) -> None:
    """
    Función auxiliar que filtra y muestra los registros con alertas activas.

    Recorre un diccionario de registros, evalúa las alertas de cada uno,
    y muestra solo los que tienen al menos una alerta activa.

    Se usa en _submenu_historial_alertas() para evitar repetir el mismo
    código en cada opción del submenú.

    Parámetros:
        registros (dict): Diccionario de registros a evaluar.
        titulo (str): Título que se mostrará en el encabezado.

    No devuelve ningún valor.
    """
    limpiar_pantalla()
    mostrar_encabezado(f"🚨 {titulo}")

    if not registros:
        mostrar_advertencia("No hay registros para este filtro.")
        console.input("\n[dim]Pulsa Enter para volver...[/dim]")
        return

    # ==============================
    # EVALUAMOS ALERTAS DE CADA REGISTRO
    # ==============================

    registros_con_alertas = []

    for clave, registro in registros.items():
        # evaluate_alerts devuelve {"messages": [...], "results": {...}}
        # También puede que el registro ya tenga alerts guardado
        # Usamos el guardado si existe, si no lo evaluamos en tiempo real
        alertas_guardadas = registro.get("alerts", {})
        if alertas_guardadas:
            mensajes = alertas_guardadas.get("messages", [])
        else:
            mensajes = evaluate_alerts(registro).get("messages", [])

        # Solo añadimos los que tienen alertas
        if mensajes:
            registros_con_alertas.append({
                "registro": registro,
                "alertas": mensajes
            })

    # ==============================
    # MOSTRAMOS LOS RESULTADOS
    # ==============================

    if not registros_con_alertas:
        mostrar_exito("¡Sin alertas! Todos los registros están dentro de los rangos normales.")
    else:
        console.print(
            f"\n[bold red]Se encontraron {len(registros_con_alertas)} "
            f"registro(s) con alertas:[/bold red]\n"
        )

        for item in registros_con_alertas:
            r = item["registro"]
            mostrar_separador()
            # Mostramos ciudad, zona y fecha de cada registro con alerta
            console.print(
                f"[bold]{r.get('city', '?')}[/bold] "
                f"[dim]({r.get('zone', '?')}) — {r.get('timestamp', '?')}[/dim]"
            )
            mostrar_tabla_alertas(item["alertas"])

    console.input("\n[dim]Pulsa Enter para volver...[/dim]")


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