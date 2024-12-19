import pytest
from sensors.humidity import HumiditySensor

@pytest.fixture
def sample_humidity_data():
    """
    Fixture providing sample humidity data for testing.
    """
    return [60, 65, 63, 70, 75]

def test_max_humidity(sample_humidity_data):
    """
    Test the calculation of maximum humidity.
    """
    humidity_sensor = HumiditySensor(sensor_id=2, location="Kosice")
    max_humidity = humidity_sensor.process_data(sample_humidity_data)
    assert max_humidity == 75, "Maximum humidity calculation is incorrect."

def test_empty_humidity_data():
    """
    Test that processing empty data raises a ValueError.
    """
    humidity_sensor = HumiditySensor(sensor_id=2, location="Kosice")
    with pytest.raises(ValueError, match="No humidity data provided."):
        humidity_sensor.process_data([])