from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseSensor(ABC):
    """
    Abstract base class for sensors.

    Attributes:
        sensor_id (int): Unique identifier for the sensor.
        location (str): Location where the sensor is deployed.
        status (str): Status of the sensor ('active', 'inactive', etc.).
    """
    
    def __init__(self, sensor_id: int, location: str, status: str = "active", source: str = "file", data_file_path: str = "data/data.json", api_url: str = "") -> None:
        """
        Initialize the base sensor with common attributes.

        Args:
            sensor_id (int): Unique identifier for the sensor.
            location (str): Location where the sensor is deployed.
            status (str): Status of the sensor. Default is 'active'.
            source (str): Source of the sensor data. Default is 'file'.
            data_file_path (str): Path to the file containing sensor data. Default is 'data/sensors_data.json'.
            api_url (str): URL to fetch sensor data from an API. Default is an empty string.
        """
        self.sensor_id = sensor_id
        self.location = location
        self.status = status
        self.source = source
        self.data_file_path = data_file_path
        self.api_url = api_url
        self.last_data = None

    def __str__(self) -> str:
        """
        Return a string representation of the sensor.

        Returns:
            str: Description of the sensor.
        """
        return f"Sensor ID: {self.sensor_id}, Location: {self.location}, Status: {self.status}"

    def get_status(self) -> str:
        """
        Get the current status of the sensor.

        Returns:
            str: The current status of the sensor.
        """
        return self.status

    def set_status(self, new_status: str) -> None:
        """
        Set a new status for the sensor.

        Args:
            new_status (str): New status to assign to the sensor.
        """
        self.status = new_status
        
    def get_data(self) -> Any:
        """
        Get the last data read by the sensor.

        Returns:
            Any: The last data read by the sensor.
        """
        return self.last_data
    
    def read_data(self) -> Any:
        """
        Read data from the sensor.

        Returns:
            Any: The data read by the sensor.
        """
        if self.status != "active":
            raise RuntimeError(f"Sensor {self.sensor_id} is not active")
        
        if self.source == "file":
            self.read_data_from_file()
        elif self.source == "api":
            self.read_data_from_api()
        else:
            raise ValueError(f"Invalid source: {self.source}")
        
    @abstractmethod
    def read_data_from_file(self) -> Any:
        """
        Abstract method to read sensor data from a file.
        """
        pass
    
    @abstractmethod
    def read_data_from_api(self) -> Any:
        """
        Abstract method to read sensor data from an API.
        """
        pass
