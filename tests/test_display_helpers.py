"""
test_display_helpers.py

Tests muy sencillos para funciones visuales del CLI.

Ejecutar:
    pytest test_display_helpers.py -v
"""


def test_mostrar_error_imprime_mensaje(capsys):
    """
    Comprueba que mostrar_error imprime el mensaje recibido.
    """
    from cli.display_helpers import mostrar_error

    mostrar_error("Error de prueba")

    capturado = capsys.readouterr()

    assert "Error de prueba" in capturado.out


def test_mostrar_exito_imprime_mensaje(capsys):
    """
    Comprueba que mostrar_exito imprime el mensaje recibido.
    """
    from cli.display_helpers import mostrar_exito

    mostrar_exito("Operación correcta")

    capturado = capsys.readouterr()

    assert "Operación correcta" in capturado.out


def test_mostrar_advertencia_imprime_mensaje(capsys):
    """
    Comprueba que mostrar_advertencia imprime el mensaje recibido.
    """
    from cli.display_helpers import mostrar_advertencia

    mostrar_advertencia("Advertencia de prueba")

    capturado = capsys.readouterr()

    assert "Advertencia de prueba" in capturado.out


def test_mostrar_info_imprime_mensaje(capsys):
    """
    Comprueba que mostrar_info imprime el mensaje recibido.
    """
    from cli.display_helpers import mostrar_info

    mostrar_info("Información de prueba")

    capturado = capsys.readouterr()

    assert "Información de prueba" in capturado.out


def test_mostrar_tabla_historico_vacio(capsys):
    """
    Comprueba que si el histórico está vacío, se muestra un aviso.
    """
    from cli.display_helpers import mostrar_tabla_historico

    mostrar_tabla_historico({})

    capturado = capsys.readouterr()

    assert "No hay registros" in capturado.out