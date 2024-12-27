import pytest
from sensors.temperature import TemperatureSensor
from unittest.mock import patch, MagicMock

@pytest.fixture
def temp_sensor_bratislava() -> TemperatureSensor:
    """
    Create a temperature sensor for Bratislava.

    Returns:
        TemperatureSensor: A temperature sensor for Bratislava.
    """
    sensor = TemperatureSensor(0, "Bratislava", source="file", data_file_path="../data/data.json")
    sensor.read_data()
    return sensor

def test_temperature_type(temp_sensor_bratislava: TemperatureSensor) -> None:
    """
    Test if the temperature is numeric.
    """
    temp = temp_sensor_bratislava.get_data()
    assert isinstance(temp, (float, int)), "Temperature should be numeric."

def test_temperature_reasonable_range(temp_sensor_bratislava) -> None:
    """
    Test if the temperature is in a reasonable range for Earth.
    """
    temp = temp_sensor_bratislava.get_data()
    assert -90 <= temp <= 60, f"Temperature {temp} is out of realistic Earth range!"


def test_temperature_invalid_location() -> None:
    """
    Test if the temperature sensor raises an exception for an invalid location.
    """
    sensor = TemperatureSensor(0, "Atlantis", source="file", data_file_path="../data/data.json")
    with pytest.raises(KeyError):
        sensor.read_data()

def test_temperature_file_not_found() -> None:
    """
    Test if the temperature sensor raises an exception for a non-existent file.
    """
    sensor = TemperatureSensor(0, "Bratislava", source="file", data_file_path="non_existent.json")
    with pytest.raises(RuntimeError):
        sensor.read_data()

@pytest.mark.parametrize("celsius_input, expected_fahrenheit", [
    (0, 32),
    (10, 50),
    (25, 77),
    (-40, -40),
])
def test_convert_to_fahrenheit(celsius_input: float, expected_fahrenheit: float) -> None:
    """
    Test the conversion from Celsius to Fahrenheit.

    Args:
        celsius_input (float): Celsius temperature.
        expected_fahrenheit (float): Expected Fahrenheit temperature.
    """
    sensor = TemperatureSensor(0, "TestCity", source="file")
    sensor.last_data = celsius_input
    assert sensor.convert_to_fahrenheit() == pytest.approx(expected_fahrenheit, 0.1)

@patch("sensors.temperature.requests.get")
def test_temperature_read_data_from_api(mock_get: MagicMock) -> None:
    """
    Test if the temperature sensor reads data from an API.

    Args:
        mock_get (MagicMock): Mocked requests.get function.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 15.5}
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    sensor = TemperatureSensor(0, "Dolny Kubin", source="api", api_url="")
    sensor.read_data()
    assert sensor.get_data() == 15.5
    assert mock_get.called