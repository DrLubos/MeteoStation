from sensors.base_sensor import BaseSensor

class TemperatureSensor(BaseSensor):
    """
    Temperature sensor class that inherits from BaseSensor.
    """

    def process_data(self, data: list[float]) -> float:
        """
        Calculate the average temperature from a list of readings.

        Args:
            data (List[float]): List of temperature readings.

        Returns:
            float: The average temperature.
        """
        if not data:
            raise ValueError("No temperature data provided.")
        avg_temp = sum(data) / len(data)
        self.update_value(avg_temp)
        return avg_temp