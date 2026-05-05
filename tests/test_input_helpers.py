"""
tests/test_input_helpers.py

Tests de cli/input_helpers.py

CÓMO EJECUTAR:
    pytest tests/test_input_helpers.py -v

CONCEPTO CLAVE:
    monkeypatch → sustituye input() para simular lo que escribe el usuario.

    Ejemplo:
        monkeypatch.setattr("builtins.input", lambda _: "25.0")
        → cada vez que el código llame a input(), devolverá "25.0"

    Para simular varios intentos:
        respuestas = iter(["malo", "25.0"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))
        → primer input() → "malo", segundo → "25.0"
"""

import pytest
from datetime import datetime


# ==============================
# TESTS
# ==============================

class TestInputHelpers:
    """Tests de las funciones de input y validación de input_helpers.py"""

    # ==============================
    # pedir_float
    # ==============================

    def test_pedir_float_valor_valido(self, monkeypatch):
        """Debe devolver el número correcto si está dentro del rango."""
        from cli.input_helpers import pedir_float

        monkeypatch.setattr("builtins.input", lambda _: "25.0")

        resultado = pedir_float("Temperatura", -20, 50)
        assert resultado == 25.0

    def test_pedir_float_acepta_coma_decimal(self, monkeypatch):
        """Debe aceptar coma como separador decimal (estilo español: 25,5)."""
        from cli.input_helpers import pedir_float

        monkeypatch.setattr("builtins.input", lambda _: "25,5")

        resultado = pedir_float("Temperatura", -20, 50)
        assert resultado == 25.5

    def test_pedir_float_reintenta_con_texto(self, monkeypatch):
        """Si el usuario escribe texto, debe pedir de nuevo hasta obtener un número."""
        from cli.input_helpers import pedir_float

        respuestas = iter(["hola", "20.0"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

        resultado = pedir_float("Temperatura", -20, 50)
        assert resultado == 20.0

    def test_pedir_float_reintenta_fuera_de_rango(self, monkeypatch):
        """Si el valor está fuera del rango, debe pedir de nuevo."""
        from cli.input_helpers import pedir_float

        respuestas = iter(["999", "30.0"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

        resultado = pedir_float("Temperatura", -20, 50)
        assert resultado == 30.0

    # ==============================
    # pedir_temperatura / humedad / viento / lluvia
    # ==============================

    def test_pedir_temperatura_valor_correcto(self, monkeypatch):
        """pedir_temperatura() debe aceptar valores entre -20 y 50."""
        from cli.input_helpers import pedir_temperatura

        monkeypatch.setattr("builtins.input", lambda _: "37.5")

        resultado = pedir_temperatura()
        assert resultado == 37.5

    def test_pedir_humedad_valor_correcto(self, monkeypatch):
        """pedir_humedad() debe aceptar valores entre 0 y 100."""
        from cli.input_helpers import pedir_humedad

        monkeypatch.setattr("builtins.input", lambda _: "75.0")

        resultado = pedir_humedad()
        assert resultado == 75.0

    def test_pedir_viento_valor_correcto(self, monkeypatch):
        """pedir_viento() debe aceptar valores entre 0 y 200."""
        from cli.input_helpers import pedir_viento

        monkeypatch.setattr("builtins.input", lambda _: "50.0")

        resultado = pedir_viento()
        assert resultado == 50.0

    def test_pedir_lluvia_valor_correcto(self, monkeypatch):
        """pedir_lluvia() debe aceptar valores entre 0 y 500."""
        from cli.input_helpers import pedir_lluvia

        monkeypatch.setattr("builtins.input", lambda _: "12.0")

        resultado = pedir_lluvia()
        assert resultado == 12.0

    # ==============================
    # pedir_fecha
    # ==============================

    def test_pedir_fecha_enter_devuelve_fecha_actual(self, monkeypatch):
        """
        Si el usuario pulsa Enter sin escribir nada,
        debe devolver la fecha y hora actual en formato YYYY-MM-DD HH:MM.
        """
        from cli.input_helpers import pedir_fecha

        monkeypatch.setattr("builtins.input", lambda _: "")

        resultado = pedir_fecha()

        # Comprobamos que el formato es correcto intentando parsearlo
        try:
            datetime.strptime(resultado, "%Y-%m-%d %H:%M")
            formato_correcto = True
        except ValueError:
            formato_correcto = False

        assert formato_correcto

    def test_pedir_fecha_formato_valido(self, monkeypatch):
        """Debe aceptar una fecha en formato YYYY-MM-DD HH:MM."""
        from cli.input_helpers import pedir_fecha

        monkeypatch.setattr("builtins.input", lambda _: "2026-05-04 18:30")

        resultado = pedir_fecha()
        assert resultado == "2026-05-04 18:30"

    def test_pedir_fecha_rechaza_formato_incorrecto(self, monkeypatch):
        """Si el formato es incorrecto, debe pedir de nuevo."""
        from cli.input_helpers import pedir_fecha

        # Primero formato incorrecto, luego correcto
        respuestas = iter(["04/05/2026", "2026-05-04 18:30"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

        resultado = pedir_fecha()
        assert resultado == "2026-05-04 18:30"

    # ==============================
    # pedir_texto
    # ==============================

    def test_pedir_texto_acepta_longitud_correcta(self, monkeypatch):
        """Debe aceptar texto con longitud igual o mayor al mínimo."""
        from cli.input_helpers import pedir_texto

        monkeypatch.setattr("builtins.input", lambda _: "elizabeth")

        resultado = pedir_texto("Nombre", longitud_min=3)
        assert resultado == "elizabeth"

    def test_pedir_texto_reintenta_si_muy_corto(self, monkeypatch):
        """Si el texto es más corto que el mínimo, debe pedir de nuevo."""
        from cli.input_helpers import pedir_texto

        # "ab" tiene 2 caracteres → rechazado (mínimo 3)
        respuestas = iter(["ab", "elizabeth"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

        resultado = pedir_texto("Nombre", longitud_min=3)
        assert resultado == "elizabeth"

    # ==============================
    # pedir_opcion_menu
    # ==============================

    def test_pedir_opcion_menu_opcion_valida(self, monkeypatch):
        """Debe aceptar una opción que esté en la lista de válidas."""
        from cli.input_helpers import pedir_opcion_menu

        monkeypatch.setattr("builtins.input", lambda _: "3")

        resultado = pedir_opcion_menu(["1", "2", "3", "4", "5"])
        assert resultado == "3"

    def test_pedir_opcion_menu_rechaza_invalida(self, monkeypatch):
        """Si la opción no está en la lista, debe pedir de nuevo."""
        from cli.input_helpers import pedir_opcion_menu

        respuestas = iter(["9", "2"])
        monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

        resultado = pedir_opcion_menu(["1", "2", "3"])
        assert resultado == "2"