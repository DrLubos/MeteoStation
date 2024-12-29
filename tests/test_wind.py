import pytest
from unittest.mock import patch, MagicMock
from sensors.wind import WindSensor

@pytest.fixture
def wind_sensor_bratislava() -> WindSensor:
    """
    Create a WindSensor instance for Bratislava from a file.

    Returns:
        WindSensor: A WindSensor instance.
    """
    sensor = WindSensor(
        sensor_id="wind_ba",
        location="Bratislava",
        source="file",
        data_file_path="../data/data.json"
    )
    return sensor


def test_wind_read_from_file_valid(wind_sensor_bratislava: WindSensor) -> None:
    """
    Test reading wind data from a file for Bratislava.

    Args:
        wind_sensor_bratislava (WindSensor): A WindSensor instance for Bratislava.
    """
    wind_sensor_bratislava.read_data()
    data = wind_sensor_bratislava.get_data()
    assert isinstance(data, dict), "Wind data should be a dictionary."
    assert "speed" in data and "deg" in data and "gust" in data, "Missing keys in wind data."


def test_wind_inactive_error(wind_sensor_bratislava: WindSensor) -> None:
    """
    Test if the sensor raises a RuntimeError when inactive.

    Args:
        wind_sensor_bratislava (WindSensor): A WindSensor instance for Bratislava.
    """
    wind_sensor_bratislava.set_status("inactive")
    with pytest.raises(RuntimeError):
        wind_sensor_bratislava.read_data()


def test_wind_missing_location() -> None:
    """
    Test if the sensor raises a KeyError when the location is missing in the data file.
    """
    sensor = WindSensor(
        sensor_id="wind_none",
        location="UnknownCity",
        source="file",
        data_file_path="../data/data.json"
    )
    with pytest.raises(KeyError):
        sensor.read_data()


def test_wind_file_not_found() -> None:
    """
    Test if the sensor raises a RuntimeError when the data file is not found.
    """
    sensor = WindSensor("wind_nf", "Bratislava", "file", "does_not_exist.json")
    with pytest.raises(RuntimeError):
        sensor.read_data()


@pytest.mark.parametrize("speed, expected_kmh", [
    (3.5, 12.6),
    (0, 0),
    (10, 36),
    (5.5, 19.8)
])
def test_wind_convert_speed_to_kmh(wind_sensor_bratislava: WindSensor, speed: float, expected_kmh: float) -> None:
    """
    Test conversion of wind speed from m/s to km/h.
    
    Args:
        wind_sensor_bratislava (WindSensor): A WindSensor instance for Bratislava.
        speed (float): Wind speed in m/s.
        expected_kmh (float): Expected wind speed in km/h.
    """
    wind_sensor_bratislava.read_data()
    wind_sensor_bratislava.last_data["speed"] = speed
    kmh = wind_sensor_bratislava.convert_speed_to_kmh()
    assert isinstance(kmh, float), "Converted speed should be a float."
    assert kmh == pytest.approx(expected_kmh, 0.1), f"Expected ~{expected_kmh} km/h but got {kmh}."


@patch("sensors.wind.requests.get")
def test_wind_read_from_api_valid(mock_get: MagicMock) -> None:
    """
    Test reading wind data from an API.

    Args:
        mock_get (MagicMock): A MagicMock object for the requests.get function.
    """
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "wind": {"speed": 2.0, "deg": 100, "gust": 3.1}
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    sensor = WindSensor(
        sensor_id="wind_api_test",
        location="Zilina",
        source="api",
        api_url="https://fake.url"
    )
    sensor.read_data()

    data = sensor.get_data()
    assert data["speed"] == 2.0
    assert data["deg"] == 100
    assert data["gust"] == 3.1


@patch("sensors.wind.requests.get")
def test_wind_read_from_api_missing_keys(mock_get: MagicMock) -> None:
    """
    Test reading wind data from an API when the response is missing keys.

    Args:
        mock_get (MagicMock): A MagicMock object for the requests.get function.
    """
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "wind": {"speed": 2.0, "deg": 120}
    }
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    sensor = WindSensor(
        sensor_id="wind_api_missing",
        location="Kosice",
        source="api",
        api_url="https://fake.url"
    )
    with pytest.raises(RuntimeError):
        sensor.read_data()