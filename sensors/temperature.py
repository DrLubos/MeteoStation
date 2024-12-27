from sensors.base_sensor import BaseSensor
import json
import requests

class TemperatureSensor(BaseSensor):
    """
    Temperature sensor class that inherits from BaseSensor.
    """
    
    def read_data_from_file(self) -> None:
        """
        Read temperature data from a file.
        """
        try:
            with open(self.data_file_path, "r") as file:
                all_data = json.load(file)
                city_data = all_data["city_data"].get(self.location)
                if city_data is None:
                    self.last_data = None
                    raise KeyError(f"Location {self.location} not found in data file")
                else:
                    self.last_data = city_data.get("temp", None)
                    if self.last_data is None:
                        raise KeyError(f"No 'temp' key for location {self.location}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from file: {e}")

    def read_data_from_api(self) -> None:
        """
        Read temperature data from an API.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            all_data = response.json()
            if "main" in all_data and "temp" in all_data["main"]:
                self.last_data = all_data["main"]["temp"]
            else:
                self.last_data = None
                raise KeyError("No 'main.temp' key in API response")
        except (requests.RequestException, KeyError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from API: {e}")

    def convert_to_fahrenheit(self) -> float:
        """
        Convert the last data read by the sensor to Fahrenheit.

        Returns:
            float: The last data read by the sensor in Fahrenheit.
        """
        if self.last_data is None:
            return None
        return self.last_data * 9/5 + 32