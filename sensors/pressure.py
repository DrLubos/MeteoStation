from sensors.base_sensor import BaseSensor

class PressureSensor(BaseSensor):
    """
    Pressure sensor class that inherits from BaseSensor.
    """

    def process_data(self, data: list[float]) -> str:
        """
        Determine the trend of pressure changes.

        Args:
            data (List[float]): List of pressure readings.

        Returns:
            str: The trend ("increasing", "decreasing", or "stable").
        """
        if len(data) < 2:
            raise ValueError("Not enough data to determine pressure trend.")
        trend = "stable"
        if data[-1] > data[0]:
            trend = "increasing"
        elif data[-1] < data[0]:
            trend = "decreasing"
        self.update_value(trend)
        return trend