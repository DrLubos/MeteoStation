import pytest
from sensors.pressure import PressureSensor

@pytest.fixture
def pressure_sensor_kosice() -> PressureSensor:
    """
    Create a pressure sensor for Kosice.

    Returns:
        PressureSensor: A pressure sensor for Kosice.
    """
    sensor = PressureSensor(0, "Kosice", source="file", data_file_path="../data/data.json")
    sensor.read_data()
    return sensor

def test_pressure_type(pressure_sensor_kosice: PressureSensor) -> None:
    """
    Test if the pressure is numeric.
    """
    pressure = pressure_sensor_kosice.get_data()
    assert isinstance(pressure, (float, int)), "Pressure should be numeric."

def test_pressure_range(pressure_sensor_kosice) -> None:
    """
    Test if the pressure is in a reasonable range for Earth.
    """
    pressure = pressure_sensor_kosice.get_data()
    assert 800 <= pressure <= 1100, f"Pressure {pressure} hPa is out of typical Earth range!"

def test_pressure_invalid_location() -> None:
    """
    Test if the pressure sensor raises an exception for an invalid location.
    """
    sensor = PressureSensor(0, "Atlantis", source="file", data_file_path="../data/data.json")
    with pytest.raises(KeyError):
        sensor.read_data()

def test_pressure_missing_file():
    sensor = PressureSensor(0, "Kosice", source="file", data_file_path="non_existent.json")
    with pytest.raises(RuntimeError):
        sensor.read_data()

def test_convert_to_psi(pressure_sensor_kosice: PressureSensor) -> None:
    """
    Test the conversion of pressure from hPa to PSI.
    """
    pressure_sensor_kosice.last_data = 1013.25
    psi = pressure_sensor_kosice.convert_to_psi()
    assert psi == pytest.approx(14.6959, rel=1e-3), f"Pressure in PSI {psi} is incorrect."

def test_convert_to_psi_no_data(pressure_sensor_kosice: PressureSensor) -> None:
    """
    Test the conversion to PSI when there is no data.
    """
    pressure_sensor_kosice.last_data = None
    psi = pressure_sensor_kosice.convert_to_psi()
    assert psi is None, "Pressure in PSI should be None when there is no data."
