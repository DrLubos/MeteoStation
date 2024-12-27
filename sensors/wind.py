from sensors.base_sensor import BaseSensor
import json
import requests

class WindSensor(BaseSensor):
    """
    Wind sensor class that inherits from BaseSensor.
    """

    def read_data_from_file(self) -> None:
        """
        Read wind data from a file.
        """
        try:
            with open(self.data_file_path, "r") as file:
                all_data = json.load(file)
                city_data = all_data["city_data"].get(self.location)
                if city_data is None:
                    self.last_data = None
                    raise KeyError(f"Location {self.location} not found in data file")
                else:
                    wind_speed = city_data.get("wind_speed", None)
                    wind_deg = city_data.get("wind_deg", None)
                    wind_gust = city_data.get("wind_gust", None)
                    self.last_data = {"speed": wind_speed, "deg": wind_deg, "gust": wind_gust}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from file: {e}")

    def read_data_from_api(self) -> None:
        """
        Read wind data from an API.
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            all_data = response.json()
            wind_data = all_data.get("wind", {})
            if "speed" not in wind_data or "deg" not in wind_data or "gust" not in wind_data:
                self.last_data = None
                raise KeyError("No 'wind.speed', 'wind.deg' or 'wind.gust' key in API response")
            self.last_data = {"speed": wind_data["speed"], "deg": wind_data["deg"], "gust": wind_data["gust"]}
        except (requests.RequestException, KeyError) as e:
            self.last_data = None
            raise RuntimeError(f"Error reading data from API: {e}")

    def convert_speed_to_kmh(self) -> float:
        """
        Convert wind speed (m/s) to km/h.
        Returns None if last_data is None or speed not present.
        """
        if not self.last_data or "speed" not in self.last_data:
            return None
        return self.last_data["speed"] * 3.6

    def __str__(self):
        """
        Return a string representation of the sensor.
        """
        return f"Wind sensor for location {self.location} with last data: Wind speed {self.last_data['speed']} m/s, Wind direction {self.last_data['deg']} degrees, Wind gust {self.last_data['gust']} m/s"