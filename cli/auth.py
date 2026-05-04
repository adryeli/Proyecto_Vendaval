"""
cli/auth.py

Módulo de autenticación del sistema Vendaval.

Responsabilidades:
- Mostrar el menú de acceso (login / registro / salir).
- Registrar nuevos usuarios con contraseña hasheada (segura).
- Validar el login de usuarios existentes.
- Guardar y cargar usuarios desde un archivo JSON.

¿Qué es un hash?
Un hash es una forma de guardar contraseñas de forma segura.
En lugar de guardar "mi_contraseña" tal cual, guardamos su "huella digital" (hash).
Así, aunque alguien robe el archivo de usuarios, no puede saber las contraseñas reales.
Usamos la librería hashlib que viene incluida en Python.
"""

# ==============================
# IMPORTACIONES
# ==============================

import json
import os
import hashlib  # Para crear el hash de la contraseña

from cli.display_helpers import (
    mostrar_encabezado,
    mostrar_exito,
    mostrar_error,
    mostrar_advertencia,
    mostrar_separador,
    limpiar_pantalla
)
from cli.input_helpers import pedir_texto, pedir_contrasena
from backend.utils.logger_config import log_info, log_warning

# ==============================
# CONFIGURACIÓN
# ==============================

# Ruta donde se guardan los usuarios registrados
# os.path.dirname(__file__) da la carpeta donde está auth.py (cli/)
# ".." sube un nivel a la raíz del proyecto
RUTA_USUARIOS = os.path.join(
    os.path.dirname(__file__), "..", "data", "users.json"
)


# ==============================
# FUNCIONES DE ALMACENAMIENTO
# ==============================

def _cargar_usuarios() -> list:
    """
    Carga la lista de usuarios desde el archivo JSON.

    El guion bajo al inicio (_) es una convención que indica que
    esta función es "privada" — solo se usa dentro de este archivo.

    No recibe parámetros.
    Devuelve:
        list: Lista de diccionarios con los usuarios registrados.
              Lista vacía si el archivo no existe o está corrupto.
    """
    # Creamos el directorio data/ si no existe
    directorio = os.path.dirname(RUTA_USUARIOS)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    if not os.path.exists(RUTA_USUARIOS):
        return []

    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _guardar_usuarios(usuarios: list) -> None:
    """
    Guarda la lista completa de usuarios en el archivo JSON.

    Parámetros:
        usuarios (list): Lista de diccionarios con todos los usuarios.

    No devuelve ningún valor.
    """
    directorio = os.path.dirname(RUTA_USUARIOS)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    with open(RUTA_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# ==============================
# FUNCIONES DE HASH
# ==============================

def _hashear_contrasena(contrasena: str) -> str:
    """
    Convierte una contraseña en texto plano a su versión hasheada (segura).

    Usa SHA-256, un algoritmo estándar y seguro incluido en Python.
    El proceso es irreversible: del hash no se puede obtener la contraseña original.

    Parámetros:
        contrasena (str): La contraseña en texto plano.

    Devuelve:
        str: La huella digital (hash) de la contraseña en formato hexadecimal.
    """
    # encode() convierte el texto a bytes (necesario para hashlib)
    # hexdigest() devuelve el hash como texto hexadecimal
    return hashlib.sha256(contrasena.encode()).hexdigest()


# ==============================
# REGISTRO DE USUARIO
# ==============================

def registrar_usuario() -> bool:
    """
    Guía al usuario por el proceso de registro con pasos numerados.

    Proceso:
    1. Pide nombre de usuario (único).
    2. Pide contraseña (mínimo 6 caracteres).
    3. Confirma la contraseña.
    4. Guarda el usuario con la contraseña hasheada.

    No recibe parámetros.
    Devuelve:
        bool: True si el registro fue exitoso, False si se canceló o falló.
    """
    limpiar_pantalla()
    mostrar_encabezado("📝 Registro de nuevo usuario", "Crea tu cuenta para acceder al sistema")

    usuarios = _cargar_usuarios()

    # ==============================
    # PASO 1: NOMBRE DE USUARIO
    # ==============================

    from rich.console import Console
    console = Console()
    console.print("\n[dim][PASO 1/3] Nombre de usuario[/dim]")
    mostrar_separador()

    while True:
        username = pedir_texto("👤 Nombre de usuario", longitud_min=3)

        # Comprobamos que el nombre de usuario no esté ya registrado
        if any(u["username"] == username for u in usuarios):
            mostrar_error(f"El usuario '{username}' ya existe. Prueba con otro nombre.")
        else:
            break

    # ==============================
    # PASO 2: CONTRASEÑA
    # ==============================

    console.print("\n[dim][PASO 2/3] Contraseña[/dim]")
    mostrar_separador()
    console.print("[dim]Mínimo 6 caracteres.[/dim]")

    while True:
        contrasena = pedir_contrasena("🔑 Contraseña")

        if len(contrasena) < 6:
            mostrar_error("La contraseña debe tener al menos 6 caracteres.")
            continue

        # ==============================
        # PASO 3: CONFIRMAR CONTRASEÑA
        # ==============================

        console.print("\n[dim][PASO 3/3] Confirmar contraseña[/dim]")
        confirmacion = pedir_contrasena("🔑 Repite la contraseña")

        if contrasena != confirmacion:
            mostrar_error("Las contraseñas no coinciden. Inténtalo de nuevo.")
            continue

        break

    # ==============================
    # GUARDAR USUARIO
    # ==============================

    nuevo_usuario = {
        "username": username,
        # Guardamos el HASH, nunca la contraseña en texto plano
        "password_hash": _hashear_contrasena(contrasena),
        # Por defecto la zona preferida está vacía; el usuario la elige al entrar
        "zona_preferida": None,
        "city_preferida": None
    }

    usuarios.append(nuevo_usuario)
    _guardar_usuarios(usuarios)

    log_info(f"Nuevo usuario registrado: {username}")
    mostrar_exito(f"¡Cuenta creada! Ya puedes iniciar sesión como '{username}'.")
    return True


# ==============================
# LOGIN
# ==============================

def iniciar_sesion() -> dict | None:
    """
    Gestiona el proceso de inicio de sesión con máximo 3 intentos.

    Proceso:
    1. Pide nombre de usuario.
    2. Pide contraseña.
    3. Compara el hash de la contraseña con el almacenado.

    No recibe parámetros.
    Devuelve:
        dict: El diccionario del usuario autenticado si el login fue correcto.
        None: Si el login falló o se agotaron los intentos.
    """
    from rich.console import Console
    console = Console()

    limpiar_pantalla()
    mostrar_encabezado("🔓 Iniciar sesión")

    usuarios = _cargar_usuarios()

    if not usuarios:
        mostrar_advertencia("No hay usuarios registrados. Regístrate primero.")
        return None

    MAX_INTENTOS = 3  # Número máximo de intentos antes de bloquear

    for intento in range(1, MAX_INTENTOS + 1):
        console.print(f"\n[dim]Intento {intento}/{MAX_INTENTOS}[/dim]")
        mostrar_separador()

        # Pedimos usuario y contraseña
        username = pedir_texto("👤 Usuario")
        contrasena = pedir_contrasena("🔑 Contraseña")

        # Hasheamos la contraseña introducida para compararla
        hash_introducido = _hashear_contrasena(contrasena)

        # Buscamos el usuario en la lista
        for usuario in usuarios:
            if usuario["username"] == username and usuario["password_hash"] == hash_introducido:
                # ¡Login correcto!
                log_info(f"Login exitoso para el usuario: {username}")
                mostrar_exito(f"Bienvenido/a, {username}! 👋")
                return usuario

        # Si llegamos aquí, el login falló
        intentos_restantes = MAX_INTENTOS - intento
        if intentos_restantes > 0:
            mostrar_error(f"Usuario o contraseña incorrectos. Te quedan {intentos_restantes} intento(s).")
        else:
            mostrar_error("Has agotado todos los intentos. Vuelve al menú de acceso.")

        log_warning(f"Intento de login fallido para el usuario: '{username}'")

    return None


# ==============================
# LOGO ASCII DEL PROYECTO
# ==============================

# Este es el logo visual de Proyecto Vendaval que aparece en la pantalla de acceso.
# Generado con la fuente "ANSI Shadow" en patorjk.com/software/taag
# Puedes cambiar la fuente entrando en esa web, escribiendo "VENDAVAL" y eligiendo otra.
LOGO_VENDAVAL = r"""
██╗   ██╗███████╗███╗   ██╗██████╗  █████╗ ██╗   ██╗ █████╗ ██╗
██║   ██║██╔════╝████╗  ██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██║
██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║██║   ██║███████║██║
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║  ██║██╔══██║╚██╗ ██╔╝██╔══██║██║
 ╚████╔╝ ███████╗██║ ╚████║██████╔╝██║  ██║ ╚████╔╝ ██║  ██║███████╗
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
"""

# Subtítulo que aparece debajo del logo
SUBTITULO = "🌪  Sistema de Monitorización Meteorológica · España"
VERSION   = "v1.0"


# ==============================
# FUNCIÓN AUXILIAR: MOSTRAR LOGO
# ==============================

def _mostrar_logo() -> None:
    """
    Muestra el logo ASCII de Proyecto Vendaval con colores en la terminal.

    Separa la responsabilidad visual del resto de la lógica:
    si mañana quieres cambiar el logo, solo tocas esta función.

    No recibe parámetros.
    No devuelve ningún valor.
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align

    console = Console()

    # Imprimimos el logo en cian brillante
    # [bold cyan] ... [/bold cyan] es la sintaxis de Rich para dar color
    console.print(f"[bold cyan]{LOGO_VENDAVAL}[/bold cyan]")

    # Panel con el subtítulo y la versión, centrado
    console.print(Panel(
        Align(
            f"[bold white]{SUBTITULO}[/bold white]\n"
            f"[dim]{VERSION}[/dim]",
            align="center"
        ),
        border_style="cyan",
        padding=(0, 4)
    ))


# ==============================
# MENÚ DE AUTENTICACIÓN
# ==============================

def mostrar_pantalla_auth() -> dict | None:
    """
    Muestra la pantalla de acceso con el logo de Proyecto Vendaval.

    Flujo:
    1. Muestra el logo ASCII del proyecto.
    2. Ofrece las opciones: iniciar sesión, registrarse o salir.
    3. Mantiene el bucle hasta que el usuario se autentica o sale.

    No recibe parámetros.
    Devuelve:
        dict: El usuario autenticado si el acceso fue correcto.
        None: Si el usuario eligió salir sin autenticarse.
    """
    from rich.console import Console
    console = Console()

    while True:
        limpiar_pantalla()

        # ==============================
        # LOGO Y CABECERA
        # ==============================

        # Llamamos a la función auxiliar que dibuja el logo
        # Si mañana quieres cambiarlo, solo editas _mostrar_logo()
        _mostrar_logo()

        # ==============================
        # OPCIONES DE ACCESO
        # ==============================

        console.print("\n[bold cyan]¿Qué quieres hacer?[/bold cyan]\n")
        console.print("  [bold]1.[/bold] 🔓 Iniciar sesión")
        console.print("  [bold]2.[/bold] 📝 Registrarse")
        console.print("  [bold]3.[/bold] 🚪 Salir\n")

        opcion = console.input("[bold yellow]▶  Elige una opción: [/bold yellow]").strip()

        # ==============================
        # NAVEGACIÓN
        # ==============================

        if opcion == "1":
            # Intentamos el login — devuelve el usuario o None si falla
            usuario = iniciar_sesion()
            if usuario is not None:
                # Login correcto → salimos del bucle y devolvemos el usuario
                return usuario
            # Si devuelve None, el bucle vuelve a mostrar el menú de acceso

        elif opcion == "2":
            # Proceso de registro — después hay que iniciar sesión manualmente
            registrar_usuario()
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")

        elif opcion == "3":
            # El usuario quiere salir sin autenticarse
            return None

        else:
            mostrar_error("Opción no válida. Escribe 1, 2 o 3.")
            console.input("\n[dim]Pulsa Enter para continuar...[/dim]")