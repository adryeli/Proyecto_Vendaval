import pytest
from unittest.mock import patch, MagicMock
from backend.scheduler.scheduler import _get_zone_for_city, start_schedule_city, start_schedule_all


def test_get_zone_for_city_encontrada():
    """Debe devolver la zona correcta para una ciudad que existe"""
    # Simulamos el contenido de zones.json
    zonas_mock = [
        {"city": "Madrid", "zone": "centro"},
        {"city": "Barcelona", "zone": "noreste"}
    ]
    with patch("builtins.open", MagicMock()), \
         patch("json.load", return_value=zonas_mock):
        resultado = _get_zone_for_city("Madrid")
        assert resultado == "centro"


def test_get_zone_for_city_no_encontrada():
    """Debe devolver None si la ciudad no está en zones.json"""
    zonas_mock = [{"city": "Madrid", "zone": "centro"}]
    with patch("builtins.open", MagicMock()), \
         patch("json.load", return_value=zonas_mock):
        resultado = _get_zone_for_city("Tokyo")
        assert resultado is None


def test_get_zone_for_city_case_insensitive():
    """La búsqueda no debe distinguir mayúsculas/minúsculas"""
    zonas_mock = [{"city": "Madrid", "zone": "centro"}]
    with patch("builtins.open", MagicMock()), \
         patch("json.load", return_value=zonas_mock):
        resultado = _get_zone_for_city("madrid")
        assert resultado == "centro"


@patch('backend.scheduler.scheduler._get_zone_for_city')
def test_start_schedule_city_ciudad_no_encontrada(mock_zone):
    """Si la ciudad no existe en zones.json el scheduler no debe arrancar"""
    mock_zone.return_value = None  # ciudad no encontrada
    # No debe lanzar excepción, simplemente no hace nada
    result = start_schedule_city("Tokyo", 60)
    assert result is None


@patch('backend.scheduler.scheduler.ingest_all_zones')
@patch('backend.scheduler.scheduler.BlockingScheduler')
def test_start_schedule_all_arranca(mock_scheduler_class, mock_ingest):
    """El scheduler de todas las zonas debe arrancar y hacer primera ingesta"""
    # Simulamos que el scheduler lanza KeyboardInterrupt al arrancar
    # para que el test no se quede bloqueado
    mock_scheduler = MagicMock()
    mock_scheduler.start.side_effect = KeyboardInterrupt
    mock_scheduler_class.return_value = mock_scheduler

    start_schedule_all(60)

    # Verificamos que se hizo la primera ingesta inmediata
    mock_ingest.assert_called()


@patch('backend.scheduler.scheduler._get_zone_for_city')
@patch('backend.scheduler.scheduler.ingest_city_weather')
@patch('backend.scheduler.scheduler.BlockingScheduler')
def test_start_schedule_city_arranca(mock_scheduler_class, mock_ingest, mock_zone):
    """El scheduler de ciudad debe arrancar y hacer primera ingesta"""
    mock_zone.return_value = "centro"
    mock_scheduler = MagicMock()
    mock_scheduler.start.side_effect = KeyboardInterrupt
    mock_scheduler_class.return_value = mock_scheduler

    start_schedule_city("Madrid", 30)

    # Verificamos que se hizo la primera ingesta inmediata
    mock_ingest.assert_called_with("Madrid", "centro")