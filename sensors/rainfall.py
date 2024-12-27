from sensors.base_sensor import BaseSensor
import json
import requests

class RainfallSensor(BaseSensor):
    """
    Rainfall sensor class that inherits from BaseSensor.
    """

    def read_data_from_file(self) -> None:
        """
        Read rainfall data from a file.
        """
        try:
            with open(self.data_file_path, "r") as file:
                all_data = json.load(file)
                city_data = all_data["city_data"].get(self.location)
                if city_data is None:
                    self.last_data = None
                    raise KeyError(f"Location {self.location} not found in data file")
                self.last_data = city_data.get("rainfall", None)
                if self.last_data is None:
                    raise KeyError(f"No 'rainfall' key for location {self.location}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from file: {e}")

    def read_data_from_api(self) -> None:
        """
        Read rainfall data from an API (interpreting clouds.all as a rainfall indicator).
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            all_data = response.json()
            clouds_data = all_data.get("clouds", {})
            if "all" not in clouds_data:
                self.last_data = None
                raise KeyError("No 'clouds.all' key in API response")
            self.last_data = clouds_data["all"]
        except (requests.RequestException, KeyError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from API: {e}")

    def is_raining(self, threshold: float = 50.0) -> bool:
        """
        Check if the last data read by the sensor is above a certain threshold.
        
        Args:
            thresold (int): Thresold value to compare the data against. Default is 50.
        
        Returns:
            bool: True if the last data is above the thresold, False otherwise.
        """
        if self.last_data is None:
            return None
        return self.last_data > threshold

    def __str__(self) -> str:
        """
        Return a string representation of the sensor.
        """
        return f"Rainfall sensor for location {self.location} with last data: {self.last_data}%"