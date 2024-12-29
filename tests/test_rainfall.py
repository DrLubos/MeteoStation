import pytest
from unittest.mock import patch, MagicMock
from sensors.rainfall import RainfallSensor

@pytest.fixture
def rainfall_sensor_bratislava() -> RainfallSensor:
    """
    Create a RainfallSensor instance for Bratislava from a file.

    Returns:
        RainfallSensor: A RainfallSensor instance.
    """
    sensor = RainfallSensor(
        sensor_id="rain_ba",
        location="Bratislava",
        source="file",
        data_file_path="../data/data.json"
    )
    return sensor


def test_rainfall_read_from_file_valid(rainfall_sensor_bratislava: RainfallSensor) -> None:
    """
    Test reading rainfall data from a file for Bratislava.

    Args:
        rainfall_sensor_bratislava (RainfallSensor): A RainfallSensor instance for Bratislava.
    """
    rainfall_sensor_bratislava.read_data()
    data = rainfall_sensor_bratislava.get_data()
    assert isinstance(data, (int, float)), "Rainfall data should be numeric."


def test_rainfall_inactive_error(rainfall_sensor_bratislava: RainfallSensor) -> None:
    """
    Test if the sensor raises a RuntimeError when inactive.

    Args:
        rainfall_sensor_bratislava (RainfallSensor): A RainfallSensor instance for Bratislava.
    """
    rainfall_sensor_bratislava.set_status("inactive")
    with pytest.raises(RuntimeError):
        rainfall_sensor_bratislava.read_data()


def test_rainfall_file_not_found() -> None:
    """
    Test if the sensor raises a RuntimeError when the data file is not found.
    """
    sensor = RainfallSensor(
        sensor_id="rain_nf",
        location="Bratislava",
        source="file",
        data_file_path="non_existent.json"
    )
    with pytest.raises(RuntimeError):
        sensor.read_data()


def test_rainfall_missing_location() -> None:
    """
    Test if the sensor raises a KeyError when the location is missing in the data file.
    """
    sensor = RainfallSensor(
        sensor_id="rain_x",
        location="NonexistentCity",
        source="file",
        data_file_path="../data/data.json"
    )
    with pytest.raises(KeyError):
        sensor.read_data()


@pytest.mark.parametrize("rain_value, threshold, expected", [
    (0, 50, False),
    (30, 50, False),
    (50, 50, False),
    (51, 50, True),
    (100, 50, True),
])
def test_is_raining_param(rain_value: float, threshold: float, expected: bool) -> None:
    """
    Test the is_raining method with different parameters

    Args:
        rain_value (float): Rainfall value
        threshold (float): Threshold value
        expected (bool): Expected result
    """
    sensor = RainfallSensor("rain_test", "CityX", source="file")
    sensor.last_data = rain_value
    result = sensor.is_raining(threshold)
    assert result == expected, f"For rainfall={rain_value} and threshold={threshold}, expected {expected} but got {result}"


@patch("sensors.rainfall.requests.get")
def test_rainfall_read_from_api_valid(mock_get: MagicMock) -> None:
    """
    Test reading rainfall data from an API.

    Args:
        mock_get (MagicMock): A MagicMock object for the requests.get function.
    """
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "clouds": {"all": 60}
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    sensor = RainfallSensor(
        sensor_id="rain_api_ok",
        location="Bratislava",
        source="api",
        api_url="https://fake.url"
    )
    sensor.read_data()
    assert sensor.get_data() == 60, "Rainfall (clouds.all) should be 60."


@patch("sensors.rainfall.requests.get")
def test_rainfall_read_from_api_missing_key(mock_get: MagicMock) -> None:
    """
    Test reading rainfall data from an API with missing keys.

    Args:
        mock_get (MagicMock): A MagicMock object for the requests.get function.
    """
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "clouds": {}
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    sensor = RainfallSensor(
        sensor_id="rain_api_missing",
        location="Zilina",
        source="api",
        api_url="https://fake.url"
    )

    with pytest.raises(RuntimeError):
        sensor.read_data()