from sensors.base_sensor import BaseSensor
import json
import requests

class PressureSensor(BaseSensor):
    """
    Pressure sensor class that inherits from BaseSensor.
    """

    def read_data_from_file(self) -> None:
        """
        Read pressure data from a file.
        """
        try:
            with open(self.data_file_path, "r") as file:
                all_data = json.load(file)
                city_data = all_data["city_data"].get(self.location)
                if city_data is None:
                    self.last_data = None
                    raise KeyError(f"Location {self.location} not found in data file")
                else:
                    self.last_data = city_data.get("pressure", None)
                    if self.last_data is None:
                        raise KeyError(f"No 'pressure' key for location {self.location}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from file: {e}")

    def read_data_from_api(self) -> None:
        """
        Read pressure data from an API.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            all_data = response.json()
            if "main" in all_data and "pressure" in all_data["main"]:
                self.last_data = all_data["main"]["pressure"]
            else:
                self.last_data = None
                raise KeyError("No 'main.pressure' key in API response")
        except (requests.RequestException, KeyError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from API: {e}")

    def convert_to_psi(self) -> float:
        """
        Convert the last data read by the sensor from hPa to PSI.

        Returns:
            float: The last data read by the sensor in PSI.
        """
        if self.last_data is None:
            return None
        return self.last_data / 68.947572932

    def __str__(self) -> str:
        """
        Return a string representation of the sensor.
        """
        return f"Pressure in {self.location}: {self.last_data} hPa"