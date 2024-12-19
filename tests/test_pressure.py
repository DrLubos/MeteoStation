import pytest
from sensors.pressure import PressureSensor

@pytest.fixture
def sample_pressure_data_increasing():
    """
    Fixture providing sample pressure data with an increasing trend.
    """
    return [1010.0, 1012.0, 1015.0]

@pytest.fixture
def sample_pressure_data_decreasing():
    """
    Fixture providing sample pressure data with a decreasing trend.
    """
    return [1015.0, 1012.0, 1010.0]

@pytest.fixture
def sample_pressure_data_stable():
    """
    Fixture providing sample pressure data with no significant changes.
    """
    return [1010.0, 1010.0, 1010.0]

def test_pressure_trend_increasing(sample_pressure_data_increasing):
    """
    Test the detection of an increasing pressure trend.
    """
    pressure_sensor = PressureSensor(sensor_id=3, location="Poprad")
    trend = pressure_sensor.process_data(sample_pressure_data_increasing)
    assert trend == "increasing", "Pressure trend detection is incorrect for increasing data."

def test_pressure_trend_decreasing(sample_pressure_data_decreasing):
    """
    Test the detection of a decreasing pressure trend.
    """
    pressure_sensor = PressureSensor(sensor_id=3, location="Poprad")
    trend = pressure_sensor.process_data(sample_pressure_data_decreasing)
    assert trend == "decreasing", "Pressure trend detection is incorrect for decreasing data."

def test_pressure_trend_stable(sample_pressure_data_stable):
    """
    Test the detection of a stable pressure trend.
    """
    pressure_sensor = PressureSensor(sensor_id=3, location="Poprad")
    trend = pressure_sensor.process_data(sample_pressure_data_stable)
    assert trend == "stable", "Pressure trend detection is incorrect for stable data."

def test_pressure_trend_insufficient_data():
    """
    Test that processing insufficient data raises a ValueError.
    """
    pressure_sensor = PressureSensor(sensor_id=3, location="Poprad")
    with pytest.raises(ValueError, match="Not enough data to determine pressure trend."):
        pressure_sensor.process_data([1010.0])