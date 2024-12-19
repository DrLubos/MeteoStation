from sensors.base_sensor import BaseSensor

class HumiditySensor(BaseSensor):
    """
    Humidity sensor class that inherits from BaseSensor.
    """

    def process_data(self, data: list[int]) -> int:
        """
        Determine the maximum humidity value.

        Args:
            data (List[int]): List of humidity readings.

        Returns:
            int: The maximum humidity value.
        """
        if not data:
            raise ValueError("No humidity data provided.")
        max_hum = max(data)
        self.update_value(max_hum)
        return max_hum