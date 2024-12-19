import pytest
from sensors.temperature import TemperatureSensor

@pytest.fixture
def sample_temperature_data():
    """
    Fixture providing sample temperature data for testing.
    """
    return [20.5, 22.0, 21.8, 19.6, 23.1]

def test_average_temperature(sample_temperature_data):
    """
    Test the calculation of average temperature.
    """
    temp_sensor = TemperatureSensor(sensor_id=1, location="Bratislava")
    avg_temp = temp_sensor.process_data(sample_temperature_data)
    assert avg_temp == pytest.approx(21.40, rel=1e-2), "Average temperature calculation is incorrect."

def test_empty_temperature_data():
    """
    Test that processing empty data raises a ValueError.
    """
    temp_sensor = TemperatureSensor(sensor_id=1, location="Bratislava")
    with pytest.raises(ValueError, match="No temperature data provided."):
        temp_sensor.process_data([])