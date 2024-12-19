from sensors.base_sensor import BaseSensor

class WindSensor(BaseSensor):
    """
    Wind sensor class that inherits from BaseSensor.
    """

    def process_data(self, data: list[float]) -> float:
        """
        Determine the maximum wind speed.

        Args:
            data (List[float]): List of wind speed readings.

        Returns:
            float: The maximum wind speed.
        """
        if not data:
            raise ValueError("No wind speed data provided.")
        max_speed = max(data)
        self.update_value(max_speed)
        return max_speed