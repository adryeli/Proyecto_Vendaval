"""
tests/test_auth_simple.py

Tests sencillos para cli/auth.py

Ejecutar:
    pytest tests/test_auth_simple.py -v
"""


# ==============================
# HELPERS DE TEST
# ==============================

def simular_input(monkeypatch, valor):
    """
    Simula lo que escribe el usuario usando Rich Console.input.
    """
    monkeypatch.setattr(
        "rich.console.Console.input",
        lambda self, *args, **kwargs: valor,
    )


def simular_varios_inputs(monkeypatch, valores):
    """
    Simula varios intentos de entrada.
    """
    respuestas = iter(valores)

    monkeypatch.setattr(
        "rich.console.Console.input",
        lambda self, *args, **kwargs: next(respuestas),
    )


# ==============================
# TESTS DE _pedir_texto_o_volver
# ==============================

def test_pedir_texto_o_volver_devuelve_volver_si_usuario_escribe_0(monkeypatch):
    """
    Comprueba que si el usuario escribe 0,
    la función devuelve el valor interno VOLVER.
    """
    from cli.auth import _pedir_texto_o_volver, VOLVER

    simular_input(monkeypatch, "0")

    resultado = _pedir_texto_o_volver("Usuario", longitud_min=3)

    assert resultado == VOLVER


def test_pedir_texto_o_volver_no_devuelve_volver_si_usuario_escribe_texto(monkeypatch):
    """
    Comprueba que si el usuario escribe un texto válido,
    NO devuelve VOLVER.
    """
    from cli.auth import _pedir_texto_o_volver, VOLVER

    simular_input(monkeypatch, "elizabeth")

    resultado = _pedir_texto_o_volver("Usuario", longitud_min=3)

    assert resultado != VOLVER
    assert resultado == "elizabeth"


def test_pedir_texto_o_volver_reintenta_si_texto_es_muy_corto(monkeypatch):
    """
    Comprueba que si el usuario escribe un texto demasiado corto,
    la función vuelve a pedir el dato.
    """
    from cli.auth import _pedir_texto_o_volver

    simular_varios_inputs(monkeypatch, ["ab", "elizabeth"])

    resultado = _pedir_texto_o_volver("Usuario", longitud_min=3)

    assert resultado == "elizabeth"
    assert resultado != "ab"


def test_pedir_usuario_elimina_espacios_laterales(monkeypatch):
    """
    Comprueba que la función elimina espacios antes y después del texto.
    """
    from cli.auth import _pedir_texto_o_volver

    simular_input(monkeypatch, "   elizabeth   ")

    resultado = _pedir_texto_o_volver("Usuario", longitud_min=3)

    assert resultado == "elizabeth"


def test_pedir_usuario_no_acepta_texto_vacio(monkeypatch):
    """
    Comprueba que si el usuario no escribe nada,
    la función vuelve a pedir el dato.
    """
    from cli.auth import _pedir_texto_o_volver

    simular_varios_inputs(monkeypatch, ["", "elizabeth"])

    resultado = _pedir_texto_o_volver("Usuario", longitud_min=3)

    assert resultado == "elizabeth"
    assert resultado != ""


def test_pedir_contrasena_no_acepta_contrasena_corta(monkeypatch):
    """
    Simula que el usuario escribe una contraseña demasiado corta.
    Después escribe una contraseña válida.
    """
    from cli.auth import _pedir_texto_o_volver

    simular_varios_inputs(monkeypatch, ["123", "PasswordSegura123"])

    resultado = _pedir_texto_o_volver("Contraseña", longitud_min=8)

    assert resultado != "123"
    assert resultado == "PasswordSegura123"


def test_pedir_contrasena_acepta_longitud_minima_exacta(monkeypatch):
    """
    Comprueba que una contraseña con exactamente 8 caracteres se acepta.
    """
    from cli.auth import _pedir_texto_o_volver

    simular_input(monkeypatch, "abc12345")

    resultado = _pedir_texto_o_volver("Contraseña", longitud_min=8)

    assert resultado == "abc12345"
    assert len(resultado) == 8

