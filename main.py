from sensors.temperature import TemperatureSensor
from utils.data_loader import DataLoader

if __name__ == "__main__":
    data = DataLoader.load_from_file("data/sensors_data.json")

    temp_sensor = TemperatureSensor(1, "Bratislava")

    avg_temp = temp_sensor.process_data(data["temperature"])
    print(f"Average temperature: {avg_temp:.2f}°C")