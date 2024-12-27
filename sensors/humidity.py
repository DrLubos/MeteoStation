from sensors.base_sensor import BaseSensor
import json
import requests

class HumiditySensor(BaseSensor):
    """
    Humidity sensor class that inherits from BaseSensor.
    """

    def read_data_from_file(self) -> None:
        """
        Read humidity data from a file.
        """
        try:
            with open(self.data_file_path, "r") as file:
                all_data = json.load(file)
                city_data = all_data["city_data"].get(self.location)
                if city_data is None:
                    self.last_data = None
                    raise KeyError(f"Location {self.location} not found in data file")
                else:
                    self.last_data = city_data.get("humidity", None)
                    if self.last_data is None:
                        raise KeyError(f"No 'humidity' key for location {self.location}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from file: {e}")

    def read_data_from_api(self) -> None:
        """
        Read humidity data from an API.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            all_data = response.json()
            if "main" in all_data and "humidity" in all_data["main"]:
                self.last_data = all_data["main"]["humidity"]
            else:
                self.last_data = None
                raise KeyError("No 'main.humidity' key in API response")
        except (requests.RequestException, KeyError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from API: {e}")

    def is_humid(self, thresold: float = 70.0) -> bool:
        """
        Check if the last data read by the sensor is above a certain thresold.

        Args:
            thresold (int): Thresold value to compare the data against. Default is 70.

        Returns:
            bool: True if the last data is above the thresold, False otherwise.
        """
        if self.last_data is None:
            return None
        return self.last_data > thresold
    
    def __str__(self) -> str:
        """
        Return a string representation of the sensor.
        """
        return f"Humidity in {self.location}: {self.last_data}%"