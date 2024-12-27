import pytest
from sensors.humidity import HumiditySensor

@pytest.fixture
def humidity_sensor_zilina() -> HumiditySensor:
    """
    Create a humidity sensor for Bratislava.

    Returns:
        HumiditySensor: A humidity sensor for Bratislava.
    """
    sensor = HumiditySensor(0, "Bratislava", source="file", data_file_path="../data/data.json")
    sensor.read_data()
    return sensor

def test_humidity_type(humidity_sensor_zilina: HumiditySensor) -> None:
    """
    Test if the humidity is numeric.
    """
    humidity = humidity_sensor_zilina.get_data()
    assert isinstance(humidity, (float, int)), "Humidity should be numeric."

def test_humidity_range(humidity_sensor_zilina) -> None:
    """
    Test if the humidity is in a percentage range.
    """
    humidity = humidity_sensor_zilina.get_data()
    assert 0 <= humidity <= 100, f"Humidity {humidity} is out of range!"

def test_humidity_inactive_error() -> None:
    """
    Test if the humidity sensor raises an exception for an inactive sensor.
    """
    sensor = HumiditySensor(0, "Bratislava", status="inactive", source="file", data_file_path="../data/data.json")
    with pytest.raises(RuntimeError):
        sensor.read_data()

def test_humidity_missing_location() -> None:
    """
    Test if the humidity sensor raises an exception for a missing location.
    """
    sensor = HumiditySensor(0, "Neverland", source="file", data_file_path="../data/data.json")
    with pytest.raises(KeyError):
        sensor.read_data()

@pytest.mark.parametrize("humidity_value, threshold, expected", [
    (40, 50, False),
    (60, 50, True),
    (100, 50, True),
    (0, 50, False),
])
def test_is_humid(humidity_value: float, threshold: float, expected: bool) -> None:
    """
    Test the is_humid method.

    Args:
        humidity_value (float): Input humidity value.
        threshold (float): Threshold value.
        expected (bool): Expected result.
    """
    sensor = HumiditySensor(0, "TestCity", source="file")
    sensor.last_data = humidity_value
    result = sensor.is_humid(threshold)
    assert result == expected, f"For humidity={humidity_value}, threshold={threshold}, expected={expected} but got {result}"