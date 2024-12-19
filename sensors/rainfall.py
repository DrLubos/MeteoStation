from sensors.base_sensor import BaseSensor

class RainfallSensor(BaseSensor):
    """
    Rainfall sensor class that inherits from BaseSensor.
    """

    def process_data(self, data: list[float]) -> float:
        """
        Calculate the total rainfall.

        Args:
            data (List[float]): List of rainfall measurements.

        Returns:
            float: The total rainfall.
        """
        if not data:
            raise ValueError("No rainfall data provided.")
        total_rain = sum(data)
        self.update_value(total_rain)
        return total_rain