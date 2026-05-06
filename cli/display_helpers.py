"""
cli/display_helpers.py

Funciones auxiliares para mostrar elementos visuales en la consola.

Responsabilidades:
- Pantalla de bienvenida y despedida.
- Encabezados y separadores visuales.
- Tablas de datos climáticos.
- Mensajes de éxito, error y advertencia.
- Limpiar la pantalla.

Usa la librería Rich para que todo quede bonito en la terminal.
"""

# ==============================
# IMPORTACIONES
# ==============================

import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Creamos un objeto Console que usaremos en todas las funciones
# Es el "pintor" de Rich: todo lo que queremos mostrar pasa por él
console = Console()


# ==============================
# PANTALLAS DE INICIO Y CIERRE
# ==============================

def mostrar_bienvenida() -> None:
    """
    Muestra la pantalla de bienvenida animada con el nombre del proyecto.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    # Panel con el nombre del proyecto y descripción
    # Los corchetes en Rich son para dar formato: [bold cyan] = negrita en cian
    console.print(Panel(
        "[bold cyan]🌪  PROYECTO VENDAVAL[/bold cyan]\n"
        "[dim]Sistema de Monitorización Meteorológica · España[/dim]\n\n"
        "[dim]Registra · Consulta · Alerta[/dim]",
        border_style="cyan",
        padding=(1, 4)
    ))


def mostrar_despedida() -> None:
    """
    Muestra el mensaje de cierre del sistema.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    console.print(Panel(
        "[bold green]¡Hasta pronto! 👋[/bold green]\n"
        "[dim]Los datos han sido guardados correctamente.[/dim]",
        border_style="green",
        padding=(1, 4)
    ))


def limpiar_pantalla() -> None:
    """
    Limpia la consola de forma compatible con Windows, Mac y Linux.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    # 'cls' es el comando de Windows, 'clear' es el de Linux/Mac
    os.system("cls" if os.name == "nt" else "clear")


# ==============================
# ENCABEZADOS Y SEPARADORES
# ==============================

def mostrar_encabezado(titulo: str, subtitulo: str = "") -> None:
    """
    Muestra un encabezado visual con título y subtítulo opcional.

    Parámetros:
        titulo (str): El texto principal del encabezado.
        subtitulo (str): Texto secundario opcional debajo del título.

    No devuelve ningún valor.
    """
    contenido = f"[bold white]{titulo}[/bold white]"

    # Solo añadimos el subtítulo si nos lo pasaron
    if subtitulo:
        contenido += f"\n[dim]{subtitulo}[/dim]"

    console.print(Panel(contenido, border_style="blue", padding=(0, 2)))


def mostrar_separador() -> None:
    """
    Imprime una línea separadora visual.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    console.print("[dim]─────────────────────────────────────────[/dim]")


# ==============================
# MENSAJES DE ESTADO
# ==============================

def mostrar_exito(mensaje: str) -> None:
    """
    Muestra un mensaje de éxito en verde con icono de confirmación.

    Parámetros:
        mensaje (str): El texto del mensaje de éxito.

    No devuelve ningún valor.
    """
    console.print(f"[bold green]✅  {mensaje}[/bold green]")


def mostrar_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error en rojo con icono de alerta.

    Parámetros:
        mensaje (str): El texto del mensaje de error.

    No devuelve ningún valor.
    """
    console.print(f"[bold red]❌  {mensaje}[/bold red]")


def mostrar_advertencia(mensaje: str) -> None:
    """
    Muestra un mensaje de advertencia en amarillo.

    Parámetros:
        mensaje (str): El texto del mensaje de advertencia.

    No devuelve ningún valor.
    """
    console.print(f"[bold yellow]⚠️   {mensaje}[/bold yellow]")


def mostrar_info(mensaje: str) -> None:
    """
    Muestra un mensaje informativo en azul.

    Parámetros:
        mensaje (str): El texto informativo.

    No devuelve ningún valor.
    """
    console.print(f"[bold blue]ℹ️   {mensaje}[/bold blue]")


# ==============================
# TABLAS DE DATOS CLIMÁTICOS
# ==============================

def mostrar_tabla_registro(registro: dict) -> None:
    """
    Muestra un registro climático individual en formato de tabla visual.

    Parámetros:
        registro (dict): Diccionario con los datos de un registro climático.
            Debe tener las claves: timestamp, city, zone, temperature_c,
            humidity_pct, wind_kph, rain_mm, source.

    No devuelve ningún valor.
    """
    # Creamos la tabla con Rich
    tabla = Table(
        title=f"📍 {registro.get('city', 'Desconocida')} — {registro.get('zone', '')}",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold cyan"
    )

    # Añadimos las columnas
    tabla.add_column("Campo", style="dim", width=18)
    tabla.add_column("Valor", justify="right")

    # Añadimos cada fila con su dato
    tabla.add_row("🕐 Fecha/hora", registro.get("timestamp", "—"))
    tabla.add_row("🌡  Temperatura", f"{registro.get('temperature_c', '—')} °C")
    tabla.add_row("💧 Humedad", f"{registro.get('humidity_pct', '—')} %")
    tabla.add_row("💨 Viento", f"{registro.get('wind_kph', '—')} km/h")
    tabla.add_row("🌧  Lluvia", f"{registro.get('rain_mm', '—')} mm")
    tabla.add_row("📡 Fuente", registro.get("source", "—"))

    console.print(tabla)


def mostrar_tabla_historico(registros: dict) -> None:
    """
    Muestra todos los registros del histórico en una tabla compacta.

    Parámetros:
        registros (dict): Diccionario de registros devuelto por get_all_records().
            Cada valor es un dict con los datos de un registro climático.

    No devuelve ningún valor.
    """
    if not registros:
        mostrar_advertencia("No hay registros en el histórico todavía.")
        return

    tabla = Table(
        title="📊 Histórico de Registros",
        box=box.SIMPLE_HEAD,
        border_style="blue",
        show_header=True,
        header_style="bold blue"
    )

    tabla.add_column("Fecha/Hora", style="dim", min_width=16)
    tabla.add_column("Ciudad")
    tabla.add_column("Zona")
    tabla.add_column("🌡 Temp.", justify="right")
    tabla.add_column("💧 Hum.", justify="right")
    tabla.add_column("💨 Viento", justify="right")
    tabla.add_column("🌧 Lluvia", justify="right")
    tabla.add_column("Fuente", style="dim")
    tabla.add_column("⚡ Alerts e Information", justify="center")

    for clave, r in registros.items():
        alertas = r.get("alerts", {}).get("messages", [])
        alarmas_reales = [a for a in alertas if a.startswith("Alarma:")]
        infos = [i for i in alertas if i.startswith("Información:")]

        if alarmas_reales:
            estado = f"[bold red]{len(alarmas_reales)} alarma(s)[/bold red]"
        elif infos:
            estado = f"[cyan]{len(infos)} info[/cyan]"
        else:
            estado = "[green]✅ OK[/green]"

        tabla.add_row(
            r.get("timestamp", "—"),
            r.get("city", "—"),
            r.get("zone", "—"),
            f"{r.get('temperature_c', '—')} °C",
            f"{r.get('humidity_pct', '—')} %",
            f"{r.get('wind_kph', '—')} km/h",
            f"{r.get('rain_mm', '—')} mm",
            r.get("source", "—"),
            estado
        )

    console.print(tabla)
    console.print(f"[dim]Total: {len(registros)} registros[/dim]")

def mostrar_comparativa(resultado: dict) -> None:
    """
    Muestra la comparativa entre el registro histórico y el dato actual de la API.

    Parámetros:
        resultado (dict): Dict con historico, actual y discrepancias de comparar_ciudad().

    No devuelve ningún valor.
    """
    city = resultado.get("city", "—")
    historico = resultado.get("historico", {})
    actual = resultado.get("actual", {})
    discrepancias = resultado.get("discrepancias", [])

    tabla = Table(
        title=f"🔍 Manual vs API — {city}",
        box=box.ROUNDED,
        border_style="magenta",
        show_header=True,
        header_style="bold magenta"
    )

    tabla.add_column("Campo",     style="dim", width=16)
    tabla.add_column("Histórico", justify="right",  width=16)
    tabla.add_column("Actual",    justify="right", width=16)
    tabla.add_column("Diff",    justify="right", width=16)

    campos = [
        ("temperature_c", "Temperatura", "°C"),
        ("humidity_pct",  "Humedad",      "%"),
        ("wind_kph",      "Viento",       "km/h"),
        ("rain_mm",       "Lluvia",       "mm"),
    ]

    for campo, nombre, unidad in campos:
        val_hist   = historico.get(campo, "—")
        val_actual = actual.get(campo, "—")

        if isinstance(val_hist, (int, float)) and isinstance(val_actual, (int, float)):
            diff = val_actual - val_hist
            color = "red" if abs(diff) > 5 else "green"
            diff_str = f"[{color}]{diff:+.1f}{unidad}[/{color}]"
        else:
            diff_str = "—"

        tabla.add_row(nombre, f"{val_hist}{unidad}", f"{val_actual}{unidad}", diff_str)

    tabla.add_section()
    tabla.add_row("Timestamp", historico.get("timestamp", "—"), actual.get("timestamp", "—"), "")
    tabla.add_row("Fuente",    historico.get("source", "—"),    actual.get("source", "—"),    "")

    console.print(tabla)

    if discrepancias:
        contenido = "\n".join(f"[bold yellow] {d}[/bold yellow]" for d in discrepancias)
        console.print(Panel(
            contenido,
            title="[bold yellow] Discrepancias detectadas[/bold yellow]",
            border_style="yellow",
            padding=(0, 2)
        ))
    else:
        mostrar_exito("Los datos históricos y actuales son consistentes.")

def mostrar_tabla_alertas(alertas: list) -> None:
    """
    Muestra las alertas activas de un registro en formato visual con colores.

    Parámetros:
        alertas (list): Lista de strings con los mensajes de alerta activos.

    No devuelve ningún valor.
    """
    if not alertas:
        mostrar_exito("Sin alertas activas — niveles climáticos normales.")
        return

    # Panel rojo para destacar que hay alertas
    contenido = []

    for alerta in alertas:
        if alerta.startswith("Alarma:"):
            contenido.append(f"[bold red]⚡ {alerta}[/bold red]")
        elif alerta.startswith("Información:"):
            contenido.append(f"[cyan]ℹ️ {alerta}[/cyan]")
        else:
            contenido.append(f"[white]{alerta}[/white]")

    console.print(Panel(
        "\n".join(contenido),
        title="[bold red]🚨 ALERTAS E INFORMACIÓN[/bold red]",
        border_style="white",
        padding=(0, 2)
    ))


def mostrar_tiempo_actual(registro: dict, alertas: list) -> None:
    """
    Muestra el tiempo actual de una zona con sus alertas de forma visual.
    Se usa al entrar al menú principal para dar bienvenida con datos en tiempo real.

    Parámetros:
        registro (dict): El registro más reciente de la zona del usuario.
        alertas (list): Lista de mensajes de alerta activos para ese registro.

    No devuelve ningún valor.
    """
    ciudad = registro.get("city", "tu zona")
    temp = registro.get("temperature_c", "—")
    hum = registro.get("humidity_pct", "—")
    viento = registro.get("wind_kph", "—")
    lluvia = registro.get("rain_mm", "—")
    timestamp = registro.get("timestamp", "")

    # Elegimos el color de la temperatura según si hace calor o frío
    if isinstance(temp, (int, float)):
        color_temp = "red" if temp > 35 else ("cyan" if temp < 5 else "white")
    else:
        color_temp = "white"

    contenido = (
        f"[bold]{ciudad}[/bold]  [dim]{timestamp}[/dim]\n\n"
        f"[{color_temp}]🌡  {temp} °C[/{color_temp}]   "
        f"[cyan]💧 {hum} %[/cyan]   "
        f"[blue]💨 {viento} km/h[/blue]   "
        f"[blue]🌧  {lluvia} mm[/blue]"
    )

    if alertas:
        lineas_alertas = []

        for alerta in alertas:
            if alerta.startswith("Alarma:"):
                lineas_alertas.append(f"[red]⚡ {alerta}[/red]")
            elif alerta.startswith("Información:"):
                lineas_alertas.append(f"[cyan]ℹ️ {alerta}[/cyan]")
            else:
                lineas_alertas.append(f"[white]{alerta}[/white]")

        contenido += "\n\n" + "\n".join(lineas_alertas)

    console.print(Panel(
        contenido,
        title="[bold cyan]🌍 Tiempo actual en tu zona[/bold cyan]",
        border_style="cyan",
        padding=(1, 3)
    ))


# ==============================
# CONFIRMACIONES
# ==============================

def pedir_confirmacion(pregunta: str) -> bool:
    """
    Pide al usuario que confirme una acción con s/n.

    Parámetros:
        pregunta (str): La pregunta a mostrar al usuario.

    Devuelve:
        bool: True si el usuario confirmó (s), False si canceló (n).
    """
    while True:
        respuesta = console.input(
            f"[bold yellow]{pregunta} (s/n): [/bold yellow]"
        ).strip().lower()

        if respuesta == "s":
            return True
        elif respuesta == "n":
            return False
        else:
            mostrar_error("Por favor escribe 's' para confirmar o 'n' para cancelar.")