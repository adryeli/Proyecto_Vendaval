import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
import matplotlib
matplotlib.use('Agg')  # ¡Antes de cualquier import de matplotlib.pyplot!
import matplotlib.pyplot as plt
from matplotlib.dates import num2date

# Ajusta esta ruta a la ubicación real de tu dashboard
from backend.stats.cyber_dashboard import run_dashboard

# ---------------------------------------------------------------------
# Datos de prueba (no dependen de archivos JSON)
# ---------------------------------------------------------------------
def crear_dataframe_prueba():
    np.random.seed(42)
    ciudades = ['Barcelona', 'Madrid', 'Valencia']
    zonas = ['Noreste', 'Centro', 'Levante']
    fechas = pd.date_range(
        start=pd.Timestamp.now().normalize() - pd.DateOffset(months=13),
        end=pd.Timestamp.now().normalize(),
        freq='D'
    )
    registros = []
    for ciudad, zona in zip(ciudades, zonas):
        for fecha in fechas:
            registros.append({
                'timestamp': fecha,
                'zone': zona,
                'city': ciudad,
                'temperature_c': round(np.random.uniform(5, 30), 1),
                'humidity_pct': round(np.random.uniform(30, 80), 1),
                'wind_kph': round(np.random.uniform(0, 30), 1),
                'rain_mm': round(np.random.uniform(0, 10), 1),
                'source': 'API'
            })
    return pd.DataFrame(registros).sort_values('timestamp')

# ---------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------
@patch('backend.stats.cyber_dashboard.get_available_cities')
@patch('backend.stats.cyber_dashboard.get_combined_data')
@patch('matplotlib.pyplot.show')  # <-- Evitamos que plt.show() cierre/limpie la figura
def test_dashboard_estado_inicial(mock_show, mock_get_data, mock_get_cities):
    # 1. Configurar mocks
    df_prueba = crear_dataframe_prueba()
    ciudades_prueba = sorted(df_prueba['city'].unique())  # ['Barcelona','Madrid','Valencia']

    mock_get_data.return_value = df_prueba
    mock_get_cities.return_value = ciudades_prueba

    # 2. Ejecutar el dashboard (plt.show() ahora es un mock, no hace nada)
    run_dashboard()

    # 3. Obtener la figura y el eje principal de la gráfica
    fig = plt.gcf()
    ax = fig.axes[0]   # <-- El primer eje es el del gráfico (no los widgets)

    # ---------------------------------------------------------
    # ✅ ASSERT 1: La ciudad inicial es Barcelona (primera alfabéticamente)
    # ---------------------------------------------------------
    titulo = ax.get_title()
    assert 'BARCELONA' in titulo, f"Se esperaba Barcelona en el título, pero es: {titulo}"

    # ---------------------------------------------------------
    # ✅ ASSERT 2: El rango del eje X es el año actual (1 enero – hoy)
    # ---------------------------------------------------------
    xlim = ax.get_xlim()
    inicio_real = num2date(xlim[0]).replace(tzinfo=None)
    fin_real = num2date(xlim[1]).replace(tzinfo=None)

    hoy = pd.Timestamp.now()  # con hora actual
    inicio_esperado = hoy.normalize().replace(month=1, day=1)

    assert inicio_real == inicio_esperado, \
        f"Inicio del eje X debería ser {inicio_esperado.date()}, pero es {inicio_real.date()}"
    # El final debe ser exactamente hoy (misma fecha) y no futuro
    assert fin_real.date() == hoy.date(), \
        f"Fin del eje X debería ser {hoy.date()}, pero es {fin_real.date()}"
    assert fin_real <= hoy + pd.Timedelta(seconds=1), \
        f"El fin del eje X no puede ser futuro: {fin_real}"

    # ✅ ASSERT 3: Hay al menos una línea conectora dibujada (datos presentes)
    lineas_conectoras = [l for l in ax.get_lines() if l.get_linestyle() == '-']
    assert len(lineas_conectoras) > 0, "No se ha dibujado ninguna línea de datos"

    # ---------------------------------------------------------
    # ✅ ASSERT 4: La leyenda contiene las cuatro variables con sus unidades
    # ---------------------------------------------------------
    leyenda = ax.get_legend()
    assert leyenda is not None, "Falta la leyenda"
    textos_leyenda = [t.get_text() for t in leyenda.get_texts()]
    for var, unidad in [('Temperatura', '°C'), ('Humedad', '%'), ('Viento', 'km/h'), ('Lluvia', 'mm')]:
        assert any(f"{var} ({unidad})" in txt for txt in textos_leyenda), \
            f"No se encuentra '{var} ({unidad})' en la leyenda"

    # ✅ ASSERT 5: El botón “Año” existe (la selección inicial se valida con el rango del año)
    boton_año_ax = None
    for ax_b in fig.axes:
        for child in ax_b.get_children():
            if isinstance(child, matplotlib.text.Text) and child.get_text() == 'Año':
                boton_año_ax = ax_b
                break
    assert boton_año_ax is not None, "No se encontró el botón 'Año'"

    plt.close('all')  # Limpieza final