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
    
    def __init__(self, sensor_id: int, location: str, status: str = "active") -> None:
        """
        Initialize the base sensor with common attributes.

        Args:
            sensor_id (int): Unique identifier for the sensor.
            location (str): Location where the sensor is deployed.
            status (str): Status of the sensor. Default is 'active'.
        """
        self.sensor_id = sensor_id
        self.location = location
        self.status = status
        self.current_value: Optional[Any] = None

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
        
    def update_value(self, value: Any) -> None:
        """
        Update the current value of the sensor.
        
        Args:
            value (Any): The new value to assign to the sensor.
        """
        self.current_value = value

    @abstractmethod
    def process_data(self, data: Any) -> Any:
        """
        Abstract method to process sensor data.

        Args:
            data (Any): The data to process.

        Returns:
            Any: The result of processing the data.
        """
        pass