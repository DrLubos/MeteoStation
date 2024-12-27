from sensors.temperature import TemperatureSensor
from sensors.rainfall import RainfallSensor
from sensors.pressure import PressureSensor
from sensors.wind import WindSensor
from sensors.humidity import HumiditySensor

if __name__ == "__main__":
    temp_sensor_ba = TemperatureSensor(0, "Bratislava", source="file")
    temp_sensor_ba.read_data()
    print(temp_sensor_ba)
    
    rain_sensor_za = RainfallSensor(1, "Zilina", source="file")
    rain_sensor_za.read_data()
    print(rain_sensor_za)
    
    pressure_sensor_ke = PressureSensor(2, "Kosice", source="file")
    pressure_sensor_ke.read_data()
    print(pressure_sensor_ke)
    
    wind_sensor_ba = WindSensor(3, "Bratislava", source="file")
    wind_sensor_ba.read_data()
    print(wind_sensor_ba)
    
    humidity_sensor_za = HumiditySensor(4, "Zilina", source="file")
    humidity_sensor_za.read_data()
    print(humidity_sensor_za)
    
    print("-" * 50)
    
    url = "https://api.openweathermap.org/data/2.5/weather?lat=49.2126808&lon=19.2960358&appid=e2693f0e516019c94b394c5dfab7379f&units=metric"
    temp_sensor_dk = TemperatureSensor(5, "Dolny Kubin", source="api", api_url=url)
    temp_sensor_dk.read_data()
    print(temp_sensor_dk)
    
    rain_sensor_dk = RainfallSensor(6, "Dolny Kubin", source="api", api_url=url)
    rain_sensor_dk.read_data()
    print(rain_sensor_dk)
    
    pressure_sensor_dk = PressureSensor(7, "Dolny Kubin", source="api", api_url=url)
    pressure_sensor_dk.read_data()
    print(pressure_sensor_dk)
    
    wind_sensor_dk = WindSensor(8, "Dolny Kubin", source="api", api_url=url)
    wind_sensor_dk.read_data()
    print(wind_sensor_dk)
    
    humidity_sensor_dk = HumiditySensor(9, "Dolny Kubin", source="api", api_url=url)
    humidity_sensor_dk.read_data()
    print(humidity_sensor_dk)
